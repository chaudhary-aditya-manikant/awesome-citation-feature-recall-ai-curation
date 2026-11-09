import csv
import importlib.util
import json
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "code" / "collect_openalex_candidates.py"
spec = importlib.util.spec_from_file_location("collector_integration", MODULE_PATH)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


def test_collector_writes_separated_private_and_shareable_outputs(tmp_path, monkeypatch):
    seed_file = tmp_path / "seeds.csv"
    seed_file.write_text(
        "title,doi,why_seed\nSeed,10.1000/seed,test seed\n", encoding="utf-8"
    )
    output = tmp_path / "collected"
    counter = {"n": 0}

    def fake_request(params, api_key, timeout=45, retries=5):
        counter["n"] += 1
        i = counter["n"]
        filt = params.get("filter", "")
        if filt.startswith("doi:"):
            doi = "10.1000/seed"
            title = "Seed scholarly curation paper"
            record_id = "https://openalex.org/WSEED"
        else:
            doi = f"10.1000/work{i}"
            title = f"Synthetic candidate {i}"
            record_id = f"https://openalex.org/W{i:05d}"
        rec = {
            "id": record_id,
            "doi": doi,
            "title": title,
            "publication_year": 2020,
            "publication_date": "2020-06-01",
            "cited_by_count": 5,
            "language": "en",
            "abstract_inverted_index": {"Synthetic": [0], "candidate": [1], "abstract": [2]},
            "type": "article",
            "is_retracted": False,
            "authorships": [{"author": {"id": "https://openalex.org/A1"}}],
            "referenced_works": [],
        }
        return {"meta": {"count": 1, "next_cursor": None}, "results": [rec]}, (
            "https://api.openalex.org/works?mocked=1"
        )

    monkeypatch.setattr(collector, "make_request", fake_request)
    monkeypatch.setattr(collector.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(sys, "argv", [
        "collect_openalex_candidates.py",
        "--output-dir", str(output),
        "--seeds", str(seed_file),
        "--per-route-year", "1",
        "--max-unique", "100",
        "--delay", "0.1",
    ])

    assert collector.main() == 0
    private_csv = output / "candidate_pool_private.csv"
    shareable_csv = output / "candidate_pool_shareable.csv"
    manifest = json.loads((output / "collection_manifest.json").read_text())
    query_lines = (output / "query_log.jsonl").read_text().splitlines()

    assert private_csv.exists() and shareable_csv.exists()
    with private_csv.open(newline="", encoding="utf-8") as f:
        private_rows = list(csv.DictReader(f))
    with shareable_csv.open(newline="", encoding="utf-8") as f:
        shareable_rows = list(csv.DictReader(f))
    assert len(private_rows) == len(shareable_rows) > 1
    assert "abstract" in private_rows[0] and "abstract" not in shareable_rows[0]
    assert all(row["label"] == "" for row in private_rows)
    assert all(row["label_status"] == "pending_human_review" for row in private_rows)
    assert manifest["collection_status"] == "CANDIDATES_COLLECTED"
    assert manifest["query_requests_logged"] == len(query_lines)
    assert manifest["citation_neighbourhood_requests_logged"] == 2
    assert (output / "raw_records.jsonl").exists()
    assert (output / "collection_errors.json").exists()
