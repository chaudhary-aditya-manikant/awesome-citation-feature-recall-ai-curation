#!/usr/bin/env python3
"""Collect a bounded, multi-route OpenAlex candidate pool for human screening.

This creates a PRIVATE working dataset, not adjudicated labels or an empirical
benchmark. Candidate retrieval is intentionally broad; every row still needs
human relevance screening and duplicate/version review.

The program does not use cursor paging. Each route/year request is capped at
100 records, keeping this bounded collection below OpenAlex's basic-page limit.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

API = "https://api.openalex.org"
YEAR_BANDS = [(2015, 2016), (2017, 2018), (2019, 2020), (2021, 2022), (2023, 2025)]
SELECT = ",".join([
    "id", "doi", "title", "publication_year", "publication_date",
    "cited_by_count", "language", "abstract_inverted_index", "type",
    "is_retracted", "authorships", "referenced_works"
])

SEARCH_ROUTES = [
    ("Q01_automated_literature_screening", "automated literature screening"),
    ("Q02_systematic_review_automation", "systematic review automation"),
    ("Q03_scholarly_information_retrieval", "scholarly information retrieval"),
    ("Q04_citation_based_scholarly_search", "citation-based scholarly search"),
    ("Q05_scientific_paper_recommendation", "scientific paper recommendation"),
    ("Q06_ai_assisted_evidence_synthesis", "AI-assisted evidence synthesis"),
    ("Q07_active_learning_screening", "active learning title abstract screening"),
    ("Q08_literature_based_discovery", "literature-based discovery"),
]

# These topic identifiers were used in the student's 29-30 Oct 2026 pilot.
# The script logs zero-result/invalid routes instead of silently assuming they work.
TOPIC_ROUTES = [
    ("T01_information_retrieval", "T10286"),
    ("T02_natural_language_processing", "T10181"),
    ("T03_text_document_classification", "T11550"),
    ("T04_scholarly_communication", "T13516"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_doi(value: Any) -> str:
    if value is None:
        return ""
    s = str(value).strip().lower()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s)
    s = s.removeprefix("doi:").strip()
    return s.rstrip("./ ")


def normalize_title(value: Any) -> str:
    s = str(value or "").lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def reconstruct_abstract(index: Any) -> str:
    if not isinstance(index, dict) or not index:
        return ""
    positioned = []
    for token, positions in index.items():
        if not isinstance(positions, list):
            continue
        for pos in positions:
            if isinstance(pos, int) and pos >= 0:
                positioned.append((pos, str(token)))
    positioned.sort(key=lambda x: x[0])
    return " ".join(token for _, token in positioned)


def first_author_id(record: dict[str, Any]) -> str:
    authorships = record.get("authorships") or []
    if authorships and isinstance(authorships[0], dict):
        author = authorships[0].get("author") or {}
        return str(author.get("id") or "")
    return ""


def make_request(params: dict[str, Any], api_key: str | None, timeout: int = 45,
                 retries: int = 5) -> tuple[dict[str, Any], str]:
    safe_params = dict(params)
    safe_params.setdefault("per_page", 100)
    safe_params.setdefault("select", SELECT)
    url = f"{API}/works?{urllib.parse.urlencode(safe_params, doseq=False)}"
    headers = {"User-Agent": "AITR-MNS2026008-ResearchCollection/1.0 (student research)"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    last_error: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return payload, url
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in {429, 500, 502, 503, 504}:
                body = exc.read(1000).decode("utf-8", "replace")
                raise RuntimeError(f"OpenAlex HTTP {exc.code}: {body}") from exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
        time.sleep(min(2 ** attempt, 20))
    raise RuntimeError(f"OpenAlex request failed after {retries} attempts: {last_error}")


def log_query(handle, route_id: str, params: dict[str, Any], url: str,
              payload: dict[str, Any], records: list[dict[str, Any]]) -> None:
    handle.write(json.dumps({
        "route_id": route_id,
        "query_completed_at_utc": utc_now(),
        "request_url_without_key": url,
        "parameters": params,
        "reported_count": (payload.get("meta") or {}).get("count"),
        "returned_count": len(records),
        "next_cursor_present": bool((payload.get("meta") or {}).get("next_cursor")),
    }, ensure_ascii=False) + "\n")
    handle.flush()


def load_seed_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Seed file not found: {path}")
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return [r for r in rows if normalize_doi(r.get("doi"))]


def build_tasks(per_route_year: int, seed_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for route_id, phrase in SEARCH_ROUTES:
        for band_idx, (start, end) in enumerate(YEAR_BANDS):
            sort = "publication_date:asc" if band_idx % 2 == 0 else "publication_date:desc"
            tasks.append({
                "route_id": f"{route_id}_{start}_{end}",
                "params": {"search": phrase,
                           "filter": f"publication_year:{start}-{end},has_abstract:true",
                           "sort": sort, "per_page": per_route_year},
            })
    for route_id, topic_id in TOPIC_ROUTES:
        for band_idx, (start, end) in enumerate(YEAR_BANDS):
            sort = "publication_date:asc" if band_idx % 2 == 0 else "publication_date:desc"
            tasks.append({
                "route_id": f"{route_id}_{start}_{end}",
                "params": {"filter": f"topics.id:{topic_id},publication_year:{start}-{end},has_abstract:true",
                           "sort": sort, "per_page": per_route_year},
            })
    # Seed resolution and citation neighbourhood are scheduled separately.
    for i, seed in enumerate(seed_rows, start=1):
        doi = normalize_doi(seed["doi"])
        tasks.append({"route_id": f"SEED{i:02d}_resolve", "params": {
            "filter": f"doi:{doi}", "per_page": 5}})
    random.Random(20261030).shuffle(tasks)
    return tasks


def record_to_row(record: dict[str, Any], route_id: str, captured_at: str) -> dict[str, Any]:
    doi = normalize_doi(record.get("doi"))
    abstract = reconstruct_abstract(record.get("abstract_inverted_index"))
    authorships = record.get("authorships") or []
    author_ids = []
    for authorship in authorships:
        author = (authorship or {}).get("author") or {}
        if author.get("id"):
            author_ids.append(str(author["id"]))
    return {
        "openalex_id": str(record.get("id") or ""),
        "doi": doi,
        "title": str(record.get("title") or "").strip(),
        "abstract": abstract,
        "year": record.get("publication_year"),
        "citations": record.get("cited_by_count"),
        "metadata_language": record.get("language") or "unknown",
        "abstract_available": bool(abstract.strip()),
        "type": record.get("type") or "",
        "is_retracted": record.get("is_retracted"),
        "first_author_openalex_id": author_ids[0] if author_ids else "",
        "author_openalex_ids": "|".join(author_ids),
        "source_routes": route_id,
        "collection_timestamp_utc": captured_at,
        "citation_snapshot_date": captured_at[:10],
        "label": "",
        "label_status": "pending_human_review",
        "label_rationale": "",
        "labeler_id": "",
        "label_date": "",
        "label_confidence": "",
        "language_verification_status": "unverified",
        "duplicate_cluster_id": "",
        "duplicate_review_status": "pending",
    }


def assign_duplicate_clusters(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Conservative grouping: exact DOI, then exact normalized title/year + first author.

    This assigns related rows to the same split cluster; it does not discard rows.
    Candidate duplicates remain for a human canonical-record decision.
    """
    parent = list(range(len(rows)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    doi_owner: dict[str, int] = {}
    title_author_owner: dict[tuple[str, str, str], int] = {}
    for i, row in enumerate(rows):
        doi = normalize_doi(row.get("doi"))
        if doi:
            if doi in doi_owner:
                union(i, doi_owner[doi])
            else:
                doi_owner[doi] = i
        title = normalize_title(row.get("title"))
        year = str(row.get("year") or "")
        author = str(row.get("first_author_openalex_id") or "")
        if title and year and author:
            key = (title, year, author)
            if key in title_author_owner:
                union(i, title_author_owner[key])
            else:
                title_author_owner[key] = i
    for i, row in enumerate(rows):
        root = find(i)
        # Stable cluster identifier based on canonical minimum OpenAlex ID in cluster.
        member_ids = [str(rows[j].get("openalex_id") or "") for j in range(len(rows)) if find(j) == root]
        stable = min((x for x in member_ids if x), default=f"row{i}")
        row["duplicate_cluster_id"] = stable
        row["duplicate_review_status"] = "needs_canonical_review" if len(member_ids) > 1 else "single_record"
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("data/private_collection"))
    parser.add_argument("--seeds", type=Path, default=Path("data/seed_papers.csv"))
    parser.add_argument("--per-route-year", type=int, default=100,
                        help="Maximum records per search/topic route and year band (1-100)")
    parser.add_argument("--max-unique", type=int, default=3000,
                        help="Hard ceiling on unique OpenAlex IDs")
    parser.add_argument("--delay", type=float, default=0.15,
                        help="Seconds between API calls; keep conservative for keyless use")
    args = parser.parse_args()
    if not 1 <= args.per_route_year <= 100:
        parser.error("--per-route-year must be in 1..100")
    if not 100 <= args.max_unique <= 3000:
        parser.error("--max-unique must be in 100..3000 (Prompt 07 cap)")
    if args.delay < 0.1:
        parser.error("--delay must be at least 0.10 seconds")
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise FileExistsError(f"Output folder is not empty: {args.output_dir}; use a new folder")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    api_key = os.environ.get("OPENALEX_API_KEY") or None
    seed_rows = load_seed_rows(args.seeds)
    tasks = build_tasks(args.per_route_year, seed_rows)
    seed_tasks = [t for t in tasks if t["route_id"].endswith("_resolve")]
    route_tasks = [t for t in tasks if not t["route_id"].endswith("_resolve")]
    started = utc_now()
    records: dict[str, dict[str, Any]] = {}
    raw_records: dict[str, dict[str, Any]] = {}
    seed_openalex_ids: list[tuple[str, str]] = []
    errors: list[dict[str, str]] = []
    query_log_path = args.output_dir / "query_log.jsonl"

    with query_log_path.open("w", encoding="utf-8") as log:
        # Resolve all seeds first so the citation-chasing route is not skipped
        # merely because the general search routes reach the pool ceiling.
        for task in seed_tasks:
            route_id = task["route_id"]
            params = task["params"]
            try:
                payload, url = make_request(params, api_key)
                result_list = payload.get("results") or []
                log_query(log, route_id, params, url, payload, result_list)
                captured_at = utc_now()
                for rec in result_list:
                    rec_id = str(rec.get("id") or "")
                    if not rec_id:
                        continue
                    seed_openalex_ids.append((route_id, rec_id))
                    raw_records.setdefault(rec_id, rec)
                    if rec_id not in records:
                        records[rec_id] = record_to_row(rec, route_id, captured_at)
            except Exception as exc:
                errors.append({"route_id": route_id, "error": f"{type(exc).__name__}: {exc}"})
                log.write(json.dumps({"route_id": route_id, "error": str(exc),
                                      "query_completed_at_utc": utc_now()}, ensure_ascii=False) + "\n")
            time.sleep(args.delay)

        # One-hop incoming and outgoing citation neighbourhoods from verified seeds.
        for seed_i, (seed_route, seed_id) in enumerate(seed_openalex_ids, start=1):
            if len(records) >= args.max_unique:
                break
            work_id = seed_id.rsplit("/", 1)[-1]
            for direction, filter_field in [("incoming_citers", "cites"), ("outgoing_references", "cited_by")]:
                if len(records) >= args.max_unique:
                    break
                params = {
                    "filter": f"{filter_field}:{work_id},publication_year:2015-2025,has_abstract:true",
                    "sort": "publication_date:desc" if direction == "incoming_citers" else "publication_date:asc",
                    "per_page": min(100, args.per_route_year),
                }
                route_id = f"CITATION_SEED{seed_i:02d}_{direction}"
                try:
                    payload, url = make_request(params, api_key)
                    result_list = payload.get("results") or []
                    log_query(log, route_id, params, url, payload, result_list)
                    captured_at = utc_now()
                    for rec in result_list:
                        rec_id = str(rec.get("id") or "")
                        if not rec_id:
                            continue
                        raw_records.setdefault(rec_id, rec)
                        if rec_id in records:
                            routes = set(records[rec_id]["source_routes"].split(";"))
                            routes.add(route_id)
                            records[rec_id]["source_routes"] = ";".join(sorted(routes))
                        else:
                            records[rec_id] = record_to_row(rec, route_id, captured_at)
                        if len(records) >= args.max_unique:
                            break
                except Exception as exc:
                    errors.append({"route_id": route_id, "error": f"{type(exc).__name__}: {exc}"})
                    log.write(json.dumps({"route_id": route_id, "error": str(exc),
                                          "query_completed_at_utc": utc_now()}, ensure_ascii=False) + "\n")
                time.sleep(args.delay)

        # Search and topic routes are interleaved by a fixed seed, so a hard cap
        # does not systematically exhaust one family before touching the others.
        random.Random(20261030).shuffle(route_tasks)
        for task in route_tasks:
            if len(records) >= args.max_unique:
                break
            route_id = task["route_id"]
            params = task["params"]
            try:
                payload, url = make_request(params, api_key)
                result_list = payload.get("results") or []
                log_query(log, route_id, params, url, payload, result_list)
                captured_at = utc_now()
                for rec in result_list:
                    rec_id = str(rec.get("id") or "")
                    if not rec_id:
                        continue
                    raw_records.setdefault(rec_id, rec)
                    if rec_id in records:
                        old_routes = set(records[rec_id]["source_routes"].split(";"))
                        old_routes.add(route_id)
                        records[rec_id]["source_routes"] = ";".join(sorted(old_routes))
                    else:
                        records[rec_id] = record_to_row(rec, route_id, captured_at)
                    if len(records) >= args.max_unique:
                        break
            except Exception as exc:
                errors.append({"route_id": route_id, "error": f"{type(exc).__name__}: {exc}"})
                log.write(json.dumps({"route_id": route_id, "error": str(exc),
                                      "query_completed_at_utc": utc_now()}, ensure_ascii=False) + "\n")
            time.sleep(args.delay)

    rows = assign_duplicate_clusters(list(records.values()))
    rows.sort(key=lambda r: r["openalex_id"])
    private_path = args.output_dir / "candidate_pool_private.csv"
    shareable_path = args.output_dir / "candidate_pool_shareable.csv"
    with private_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["openalex_id"])
        writer.writeheader()
        writer.writerows(rows)
    shareable_rows = [{k: v for k, v in row.items() if k != "abstract"} for row in rows]
    with shareable_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(shareable_rows[0].keys()) if shareable_rows else ["openalex_id"])
        writer.writeheader()
        writer.writerows(shareable_rows)
    with (args.output_dir / "raw_records.jsonl").open("w", encoding="utf-8") as f:
        for rec_id in sorted(raw_records):
            f.write(json.dumps(raw_records[rec_id], ensure_ascii=False) + "\n")
    with (args.output_dir / "collection_errors.json").open("w", encoding="utf-8") as f:
        json.dump(errors, f, indent=2)
    log_entries = []
    with query_log_path.open(encoding="utf-8") as log:
        for line in log:
            try:
                log_entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    summary = {
        "collection_status": "CANDIDATES_COLLECTED" if rows else "NO_RECORDS_RETURNED",
        "collection_started_utc": started,
        "collection_completed_utc": utc_now(),
        "citation_snapshot_date": started[:10],
        "openalex_api_base": API,
        "api_key_used": bool(api_key),
        "per_route_year_limit": args.per_route_year,
        "unique_openalex_works": len(rows),
        "raw_unique_records": len(raw_records),
        "candidate_records_with_abstract": sum(bool(r.get("abstract")) for r in rows),
        "candidate_records_missing_abstract": sum(not bool(r.get("abstract")) for r in rows),
        "candidate_duplicate_clusters_over_one_record": len({r["duplicate_cluster_id"] for r in rows if r["duplicate_review_status"] == "needs_canonical_review"}),
        "seed_papers_resolved": len(seed_openalex_ids),
        "query_tasks_planned": len(tasks),
        "seed_resolution_tasks": len(seed_tasks),
        "search_and_topic_tasks": len(route_tasks),
        "query_requests_logged": len(log_entries),
        "citation_neighbourhood_requests_logged": sum(str(x.get("route_id", "")).startswith("CITATION_") for x in log_entries),
        "errors": errors,
        "warning": "Candidate pool only. Labels remain blank and duplicate/version clusters require manual canonical review.",
    }
    (args.output_dir / "collection_manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    # An empty result should not be mistaken for a successful collection.
    return 0 if rows else 2


if __name__ == "__main__":
    sys.exit(main())
