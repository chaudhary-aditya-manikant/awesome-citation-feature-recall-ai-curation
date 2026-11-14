#!/usr/bin/env python3
"""Balanced, reproducible OpenAlex candidate-pool collector for AITR MNS2026008.

This script builds a candidate pool only. It does NOT assign relevance labels and
must not be used to claim human-adjudicated ground truth. It samples 8 text-search
and 4 topic routes within each exact publication year from 2015 through 2025, then
adds bounded seed DOI and citation-neighbourhood records. Abstracts stay in the
private CSV; the shareable CSV omits abstract text.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

API = "https://api.openalex.org"
YEARS = list(range(2015, 2026))
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
TOPIC_ROUTES = [
    ("T01_information_retrieval", "T10286"),
    ("T02_natural_language_processing", "T10181"),
    ("T03_text_document_classification", "T11550"),
    ("T04_scholarly_communication", "T13516"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_seed(route_id: str, base_seed: int) -> int:
    digest = hashlib.sha256(f"{base_seed}:{route_id}".encode()).digest()
    return int.from_bytes(digest[:4], "big") % 2_147_483_647


def norm_doi(v: Any) -> str:
    s = str(v or "").strip().lower()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s)
    return s.removeprefix("doi:").strip().rstrip("./ ")


def norm_title(v: Any) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", str(v or "").lower()).split())


def reconstruct_abstract(index: Any) -> str:
    if not isinstance(index, dict):
        return ""
    words = []
    for token, positions in index.items():
        if isinstance(positions, list):
            for pos in positions:
                if isinstance(pos, int) and pos >= 0:
                    words.append((pos, str(token)))
    words.sort(key=lambda x: x[0])
    return " ".join(w for _, w in words)


def make_request(params: dict[str, Any], api_key: str | None, timeout: int = 45, retries: int = 5):
    safe_query = dict(params)
    safe_query.setdefault("per_page", 100)
    safe_query.setdefault("select", SELECT)
    query = dict(safe_query)
    if api_key:
        query["api_key"] = api_key
    url = f"{API}/works?{urllib.parse.urlencode(query, doseq=False)}"
    # Build the log URL without the key, rather than trying to redact an encoded value.
    safe_url = f"{API}/works?{urllib.parse.urlencode(safe_query, doseq=False)}"
    req = urllib.request.Request(url, headers={"User-Agent": "AITR-MNS2026008-Balanced-Collector/2.0"})
    last_error = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8")), safe_url
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in {429, 500, 502, 503, 504}:
                body = exc.read(1000).decode("utf-8", "replace")
                raise RuntimeError(f"OpenAlex HTTP {exc.code}: {body}") from exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
        time.sleep(min(2 ** attempt, 20))
    raise RuntimeError(f"OpenAlex request failed after {retries} attempts: {last_error}")


def load_seed_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(f) if norm_doi(r.get("doi"))]


def build_route_tasks(per_route_year: int, base_seed: int) -> list[dict[str, Any]]:
    tasks = []
    for rid, phrase in SEARCH_ROUTES:
        for year in YEARS:
            route_id = f"{rid}_{year}"
            tasks.append({"route_id": route_id, "route_family": "search", "params": {
                "search": phrase,
                "filter": f"publication_year:{year},has_abstract:true",
                "sample": per_route_year,
                "seed": stable_seed(route_id, base_seed),
                "per_page": per_route_year,
            }})
    for rid, topic in TOPIC_ROUTES:
        for year in YEARS:
            route_id = f"{rid}_{year}"
            tasks.append({"route_id": route_id, "route_family": "topic", "params": {
                "filter": f"topics.id:{topic},publication_year:{year},has_abstract:true",
                "sample": per_route_year,
                "seed": stable_seed(route_id, base_seed),
                "per_page": per_route_year,
            }})
    return tasks


def build_citation_tasks(seed_ids: list[tuple[str, str]], sample_size: int, seed: int):
    tasks = []
    for n, (_, full_id) in enumerate(seed_ids, 1):
        work_id = full_id.rsplit("/", 1)[-1]
        for direction, filter_name in (("incoming_citers", "cites"), ("outgoing_references", "cited_by")):
            route_id = f"CITATION_SEED{n:02d}_{direction}"
            tasks.append({"route_id": route_id, "route_family": "citation_neighbourhood", "params": {
                "filter": f"{filter_name}:{work_id},publication_year:2015-2025,has_abstract:true",
                "sample": sample_size,
                "seed": stable_seed(route_id, seed),
                "per_page": sample_size,
            }})
    return tasks


def record_to_row(rec: dict[str, Any], route_id: str, snapshot_date: str, captured_at: str) -> dict[str, Any]:
    author_ids = []
    for auth in rec.get("authorships") or []:
        aid = ((auth or {}).get("author") or {}).get("id")
        if aid:
            author_ids.append(str(aid))
    abstract = reconstruct_abstract(rec.get("abstract_inverted_index"))
    return {
        "openalex_id": str(rec.get("id") or ""),
        "doi": norm_doi(rec.get("doi")),
        "title": str(rec.get("title") or "").strip(),
        "abstract": abstract,
        "year": rec.get("publication_year"),
        "citations": rec.get("cited_by_count"),
        "metadata_language": rec.get("language") or "unknown",
        "abstract_available": bool(abstract),
        "type": rec.get("type") or "",
        "is_retracted": rec.get("is_retracted"),
        "first_author_openalex_id": author_ids[0] if author_ids else "",
        "author_openalex_ids": "|".join(author_ids),
        "source_routes": route_id,
        "collection_timestamp_utc": captured_at,
        "citation_snapshot_date": snapshot_date,
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


def assign_duplicate_clusters(rows: list[dict[str, Any]], known_group_path: Path | None = None):
    """Create conservative split groups; keep all records pending human canonical review."""
    parent = list(range(len(rows)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a
    doi_owner = {}
    title_authors = {}
    for i, row in enumerate(rows):
        doi = norm_doi(row.get("doi"))
        if doi:
            if doi in doi_owner:
                union(i, doi_owner[doi])
            else:
                doi_owner[doi] = i
        title, year = norm_title(row.get("title")), str(row.get("year") or "")
        authors = tuple(sorted(filter(None, str(row.get("author_openalex_ids") or "").split("|"))))
        if title and year and authors:
            title_authors.setdefault((title, year, authors), []).append(i)
    for indexes in title_authors.values():
        for pos, i in enumerate(indexes):
            for j in indexes[pos + 1:]:
                a = " ".join(str(rows[i].get("abstract") or "").lower().split())
                b = " ".join(str(rows[j].get("abstract") or "").lower().split())
                if a and b and SequenceMatcher(None, a, b).ratio() >= 0.95:
                    union(i, j)
    manual = {}
    if known_group_path and known_group_path.exists():
        with known_group_path.open(newline="", encoding="utf-8-sig") as f:
            for item in csv.DictReader(f):
                oid = (item.get("openalex_id") or "").strip()
                gid = (item.get("duplicate_group_id") or "").strip()
                if oid and gid:
                    manual[oid] = (gid, (item.get("review_status") or "manual_review").strip())
        by_group = {}
        for i, row in enumerate(rows):
            if row.get("openalex_id") in manual:
                by_group.setdefault(manual[row["openalex_id"]][0], []).append(i)
        for idxs in by_group.values():
            for j in idxs[1:]:
                union(idxs[0], j)
    roots = {}
    for i in range(len(rows)):
        roots.setdefault(find(i), []).append(i)
    for idxs in roots.values():
        manual_groups = {manual[rows[i]["openalex_id"]][0] for i in idxs if rows[i].get("openalex_id") in manual}
        if len(manual_groups) > 1:
            raise ValueError(f"Conflicting manual groups merged: {sorted(manual_groups)}")
        if manual_groups:
            cluster = next(iter(manual_groups))
            statuses = {manual[rows[i]["openalex_id"]][1] for i in idxs if rows[i].get("openalex_id") in manual}
            status = next(iter(statuses)) if len(statuses) == 1 else "manual_group_review"
        else:
            cluster = min((str(rows[i].get("openalex_id") or "") for i in idxs), default=f"row{idxs[0]}")
            status = "auto_candidate_needs_review" if len(idxs) > 1 else "single_record"
        for i in idxs:
            rows[i]["duplicate_cluster_id"] = cluster
            rows[i]["duplicate_review_status"] = status
    return rows


def expected_max_records(per_route_year: int, per_citation: int, seed_count: int) -> int:
    return 132 * per_route_year + 2 * seed_count * per_citation + 5 * seed_count


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-dir", type=Path, default=Path("data/private_collection_balanced_20261031"))
    ap.add_argument("--seeds", type=Path, default=Path("data/seed_papers.csv"))
    ap.add_argument("--per-route-year", type=int, default=20)
    ap.add_argument("--per-citation-neighbourhood", type=int, default=30)
    ap.add_argument("--max-unique", type=int, default=3000)
    ap.add_argument("--sampling-seed", type=int, default=20261031)
    ap.add_argument("--known-duplicate-groups", type=Path, default=Path("data/known_duplicate_groups.csv"))
    ap.add_argument("--delay", type=float, default=0.20)
    args = ap.parse_args()
    if not 1 <= args.per_route_year <= 100 or not 1 <= args.per_citation_neighbourhood <= 100:
        ap.error("sample sizes must be between 1 and 100")
    if not 100 <= args.max_unique <= 3000:
        ap.error("--max-unique must be 100..3000 under the frozen pool cap")
    if args.delay < 0.1:
        ap.error("--delay must be at least 0.10 seconds")
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise FileExistsError(f"Output directory is not empty: {args.output_dir}; choose a new directory")
    if not args.seeds.exists():
        ap.error(f"Seed file not found: {args.seeds}")
    seed_rows = load_seed_rows(args.seeds)
    max_possible = expected_max_records(args.per_route_year, args.per_citation_neighbourhood, len(seed_rows))
    if max_possible > args.max_unique:
        ap.error(f"Design maximum {max_possible} exceeds cap {args.max_unique}; reduce per-route sampling")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    api_key = os.environ.get("OPENALEX_API_KEY") or None
    started = utc_now()
    snapshot_date = started[:10]
    rows_by_id: dict[str, dict[str, Any]] = {}
    raw_by_id: dict[str, dict[str, Any]] = {}
    completed, errors, resolved = [], [], []
    log_path = args.output_dir / "query_log.jsonl"

    def run_task(log, task):
        route_id, family, params = task["route_id"], task["route_family"], task["params"]
        try:
            payload, safe_url = make_request(params, api_key)
            recs = payload.get("results") or []
            log.write(json.dumps({"route_id": route_id, "route_family": family,
                "parameters": params, "request_url_without_key": safe_url,
                "reported_count": (payload.get("meta") or {}).get("count"),
                "returned_count": len(recs), "sample_seed": params.get("seed"),
                "sample_size_requested": params.get("sample"), "completed_at_utc": utc_now()}, ensure_ascii=False) + "\n")
            log.flush()
            completed.append({"route_id": route_id, "route_family": family, "returned_count": len(recs)})
            captured_at = utc_now()
            for rec in recs:
                oid = str(rec.get("id") or "")
                if not oid:
                    continue
                raw_by_id.setdefault(oid, rec)
                if oid in rows_by_id:
                    old = set(filter(None, rows_by_id[oid]["source_routes"].split(";")))
                    old.add(route_id)
                    rows_by_id[oid]["source_routes"] = ";".join(sorted(old))
                else:
                    rows_by_id[oid] = record_to_row(rec, route_id, snapshot_date, captured_at)
            return recs
        except Exception as exc:
            errors.append({"route_id": route_id, "route_family": family, "error": f"{type(exc).__name__}: {exc}"})
            log.write(json.dumps({"route_id": route_id, "route_family": family, "error": f"{type(exc).__name__}: {exc}", "completed_at_utc": utc_now()}, ensure_ascii=False) + "\n")
            log.flush()
            return []

    with log_path.open("w", encoding="utf-8") as log:
        seed_tasks = []
        for i, seed in enumerate(seed_rows, 1):
            doi = norm_doi(seed.get("doi"))
            seed_tasks.append({"route_id": f"SEED{i:02d}_resolve", "route_family": "seed_resolution",
                               "params": {"filter": f"doi:{doi}", "per_page": 5}})
        for task, seed_row in zip(seed_tasks, seed_rows):
            recs = run_task(log, task)
            target_doi = norm_doi(seed_row.get("doi"))
            exact = [r for r in recs if norm_doi(r.get("doi")) == target_doi and r.get("id")]
            if exact:
                resolved.append((task["route_id"], str(exact[0]["id"])))
            time.sleep(args.delay)
        citation_tasks = build_citation_tasks(resolved, args.per_citation_neighbourhood, args.sampling_seed)
        for task in citation_tasks:
            run_task(log, task)
            time.sleep(args.delay)
        route_tasks = build_route_tasks(args.per_route_year, args.sampling_seed)
        for task in route_tasks:
            run_task(log, task)
            time.sleep(args.delay)

    rows = assign_duplicate_clusters(list(rows_by_id.values()), args.known_duplicate_groups)
    rows.sort(key=lambda r: r["openalex_id"])
    if len(rows) > args.max_unique:
        raise RuntimeError(f"Unique IDs {len(rows)} exceeded configured cap {args.max_unique}")
    if rows:
        private_fields = list(rows[0].keys())
        with (args.output_dir / "candidate_pool_private.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=private_fields); w.writeheader(); w.writerows(rows)
        share = [{k: v for k, v in r.items() if k != "abstract"} for r in rows]
        with (args.output_dir / "candidate_pool_shareable.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(share[0].keys())); w.writeheader(); w.writerows(share)
    else:
        (args.output_dir / "candidate_pool_private.csv").write_text("openalex_id\n", encoding="utf-8")
        (args.output_dir / "candidate_pool_shareable.csv").write_text("openalex_id\n", encoding="utf-8")
    with (args.output_dir / "raw_records.jsonl").open("w", encoding="utf-8") as f:
        for oid in sorted(raw_by_id):
            f.write(json.dumps(raw_by_id[oid], ensure_ascii=False) + "\n")
    (args.output_dir / "collection_errors.json").write_text(json.dumps(errors, indent=2), encoding="utf-8")
    families = Counter(x["route_family"] for x in completed)
    manifest = {
        "collection_status": "CANDIDATES_COLLECTED_NO_API_ERRORS" if rows and not errors else "CANDIDATES_COLLECTED_WITH_API_ERRORS" if rows else "NO_RECORDS_RETURNED",
        "collection_started_utc": started, "collection_completed_utc": utc_now(),
        "citation_snapshot_date": snapshot_date, "openalex_api_base": API,
        "api_key_used": bool(api_key), "sampling_method": "OpenAlex seeded random sample within each exact query/year frame; no publication-date or citation sorting",
        "sampling_seed_base": args.sampling_seed, "publication_years": YEARS,
        "search_routes_planned": len(SEARCH_ROUTES) * len(YEARS),
        "topic_routes_planned": len(TOPIC_ROUTES) * len(YEARS),
        "search_topic_routes_planned": len(SEARCH_ROUTES + TOPIC_ROUTES) * len(YEARS),
        "search_topic_routes_executed": sum(1 for x in completed if x["route_family"] in {"search", "topic"}),
        "seed_resolution_requests_planned": len(seed_tasks),
        "seed_resolution_requests_executed": families["seed_resolution"],
        "seed_papers_resolved": len(resolved), "citation_neighbourhood_requests_planned": 2 * len(resolved),
        "citation_neighbourhood_requests_executed": families["citation_neighbourhood"],
        "route_family_counts_executed": dict(families), "unique_openalex_works": len(rows),
        "raw_unique_records": len(raw_by_id), "maximum_possible_records_under_design": max_possible,
        "candidate_records_with_abstract": sum(bool(r["abstract"]) for r in rows),
        "candidate_records_missing_abstract": sum(not bool(r["abstract"]) for r in rows),
        "candidate_duplicate_clusters_over_one_record": len({r["duplicate_cluster_id"] for r in rows if r["duplicate_review_status"] != "single_record"}),
        "errors": errors,
        "warning": "Candidate pool only. Human relevance labels and publication-language verification are not assigned by this collector. Review every duplicate cluster and eligibility flag before modelling."
    }
    (args.output_dir / "collection_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
