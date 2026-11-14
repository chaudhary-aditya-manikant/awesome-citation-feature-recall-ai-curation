#!/usr/bin/env python3
"""Build the Study 2 input from the SYNERGY benchmark (run in Colab; needs internet).

Steps
1. Read every review of the original SYNERGY dataset (26 reviews, human inclusion labels) with the
   `synergy-dataset` package. The package now defaults to the larger SYNERGY+ collection, in which many
   records have no OpenAlex id; the protocol names SYNERGY, so SYNERGY_SET=synergy is set here.
2. Fetch publication year and cited_by_count for each work from the OpenAlex API
   (batches of 100 IDs), on the citation snapshot date frozen in configs/study2_protocol.json.
3. Write one CSV (data/study2/synergy_model_input.csv) in the schema used by run_study2.py,
   plus a manifest with dataset counts, snapshot date and file hash.

Usage (Colab):
    !pip install synergy-dataset pandas requests
    !python src/study2_fetch_synergy.py --config configs/study2_protocol.json --out data/study2
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import hashlib
import json
import re
import time
from pathlib import Path

import pandas as pd

OPENALEX = "https://api.openalex.org/works"


def short_id(x: str) -> str:
    return str(x).rstrip("/").split("/")[-1]


def norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(t).lower()).strip()


def add_split_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Records with the same normalised title inside one dataset share a split group,
    so near-duplicate versions never fall on both sides of a split."""
    df = df.copy()
    key = df.dataset + "|" + df.title.map(norm_title)
    first = df.groupby(key).openalex_id.transform("first")
    df["split_group_id"] = df.dataset + "|" + first
    return df


ID_RE = r"(?i)(?:openalex\.org/)?(W\d+)"


def _pick_id(f: pd.DataFrame) -> pd.Series:
    """The column (index included) holding the most OpenAlex work ids, normalised to 'W123'."""
    best, best_n = None, 0
    for c in f.columns:
        ext = f[c].astype(str).str.extract(ID_RE, expand=False)
        n = int(ext.notna().sum())
        if n > best_n:
            best, best_n = ext.str.upper(), n
    return best if best is not None else pd.Series([None] * len(f), index=f.index)


def read_synergy(with_meta: bool = False) -> pd.DataFrame:
    """All SYNERGY reviews with title, abstract and the reviewers' inclusion label.
    With `with_meta`, also the package's stored publication_year and cited_by_count."""
    os.environ.setdefault("SYNERGY_SET", "synergy")  # original SYNERGY, as named in the protocol
    from synergy_dataset import iter_datasets  # imported here so tests need no network package
    print(f"SYNERGY_SET={os.environ['SYNERGY_SET']} SYNERGY_VERSION={os.environ.get('SYNERGY_VERSION', 'package default')}", flush=True)
    frames = []
    for d in iter_datasets():
        if with_meta:
            try:
                f = d.to_frame(vars=["title", "abstract", "publication_year", "cited_by_count"])
            except Exception as e:  # older/newer package versions name the option differently
                print(f"  {d.name}: field list not accepted ({type(e).__name__}); reading all stored fields", flush=True)
                f = d.to_frame(vars="extended")
            if not {"publication_year", "cited_by_count"} <= set(f.columns):
                raise SystemExit(f"{d.name}: stored year/citations not found. Columns: {list(f.columns)[:40]}")
        else:
            f = d.to_frame()
        f = f.reset_index()
        ids = _pick_id(f)
        n_all = len(f)
        f = f.drop(columns=[c for c in ("openalex_id",) if c in f.columns]).assign(openalex_id=ids)
        f = f[f.openalex_id.notna()]
        if f.empty:
            print(f"  {d.name}: no OpenAlex ids found. Columns: {list(f.columns)}", flush=True)
            print(d.to_frame().reset_index().head(2).to_string()[:800], flush=True)
            continue
        if len(f) < n_all:
            print(f"  {d.name}: {n_all - len(f)} records without an OpenAlex id dropped", flush=True)
        f["dataset"] = d.name
        cols = ["dataset", "openalex_id", "title", "abstract", "label_included"]
        if with_meta:
            f = f.rename(columns={"publication_year": "year", "cited_by_count": "citations"})
            cols += ["year", "citations"]
        frames.append(f[cols])
        print(f"read {d.name}: {len(f)} records, {int(f.label_included.sum())} included", flush=True)
    if not frames:
        raise SystemExit("No SYNERGY records with OpenAlex ids were read: send the printed sample to Claude.")
    df = pd.concat(frames, ignore_index=True)
    return df.rename(columns={"label_included": "label"})


def fetch_year_citations(ids, mailto):
    """OpenAlex year/citations in batches of 100, slowed down, with long waits on 429 and a resumable cache."""
    import requests
    cache = Path("data/study2/openalex_cache.csv")
    cache.parent.mkdir(parents=True, exist_ok=True)
    done = pd.read_csv(cache) if cache.exists() else pd.DataFrame(columns=["openalex_id", "year", "citations", "metadata_language"])
    have = set(done.openalex_id.astype(str))
    uniq = sorted(set(i for i in ids if isinstance(i, str)) - have)
    print(f"cached {len(have)}, still to fetch {len(uniq)}", flush=True)
    for i in range(0, len(uniq), 100):
        batch = uniq[i:i + 100]
        params = {"filter": "openalex_id:" + "|".join(batch), "per-page": 100,
                  "select": "id,publication_year,cited_by_count,language"}
        if mailto:
            params["mailto"] = mailto
        for attempt in range(15):
            r = requests.get(OPENALEX, params=params, timeout=60)
            if r.status_code == 200:
                break
            wait = min(300, 20 * (attempt + 1))
            print(f"OpenAlex {r.status_code}; waiting {wait}s (attempt {attempt + 1}/15)", flush=True)
            time.sleep(wait)
        r.raise_for_status()
        rows = [{"openalex_id": short_id(w["id"]), "year": w.get("publication_year"),
                 "citations": w.get("cited_by_count"), "metadata_language": w.get("language") or "unknown"}
                for w in r.json()["results"]]
        pd.DataFrame(rows, columns=done.columns).to_csv(cache, mode="a", header=not cache.exists() or cache.stat().st_size == 0, index=False)
        time.sleep(0.2)
        if i % 10000 == 0:
            print(f"fetched {len(have) + i + len(batch)}/{len(have) + len(uniq)}", flush=True)
    return pd.read_csv(cache).drop_duplicates("openalex_id")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--mailto", default=None, help="optional email for the OpenAlex polite pool")
    ap.add_argument("--citations", choices=["openalex", "package"], default="openalex",
                    help="openalex: live counts on the snapshot date (protocol default); package: counts stored in the SYNERGY release")
    args = ap.parse_args()
    cfg = json.loads(args.config.read_text())
    snap = cfg["data"]["citation_snapshot_date"]
    from run_study2 import undecided
    if undecided(cfg):
        raise SystemExit("Fill every DECIDE value in the protocol and commit it before fetching data.")
    today = dt.date.today().isoformat()
    if today != snap:
        print(f"WARNING: frozen snapshot date {snap} differs from today {today}; record this in the log.")

    if args.citations == "openalex":
        df = read_synergy()
        meta = fetch_year_citations(df.openalex_id.tolist(), args.mailto)
        if meta.empty:
            raise SystemExit("OpenAlex returned no records: use --citations package instead.")
        df = df.merge(meta, on="openalex_id", how="left")
    else:
        df = read_synergy(with_meta=True)
        df["metadata_language"] = "unknown"
    n0 = len(df)
    df = df.dropna(subset=["year", "citations", "title"])
    df = df.drop_duplicates(["dataset", "openalex_id"])
    df["year"] = df.year.astype(int)
    df["citations"] = df.citations.astype(int)
    df["label"] = df.label.astype(int)
    df["label_status"] = "external_benchmark_human"
    df = add_split_groups(df)

    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "synergy_model_input.csv"
    df.to_csv(path, index=False)
    manifest = {
        "source": "SYNERGY (synergy-dataset package)", "citation_source": args.citations,
        "synergy_set": os.environ.get("SYNERGY_SET"), "synergy_version": os.environ.get("SYNERGY_VERSION", "package default"),
        "fetched_on": today, "frozen_snapshot_date": snap,
        # Year the citation counts refer to: the snapshot year for live OpenAlex counts; for counts stored in
        # the SYNERGY release, the latest publication year in the data (the release's own collection year).
        "citation_reference_year": int(pd.Timestamp(snap).year) if args.citations == "openalex" else int(df.year.max()),
        "records_read": n0, "records_kept": int(len(df)), "dropped_missing_metadata": int(n0 - len(df)),
        "per_dataset": df.groupby("dataset").label.agg(records="size", included="sum").reset_index().to_dict("records"),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }
    (args.out / "synergy_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({k: v for k, v in manifest.items() if k != "per_dataset"}, indent=2))


if __name__ == "__main__":
    main()
