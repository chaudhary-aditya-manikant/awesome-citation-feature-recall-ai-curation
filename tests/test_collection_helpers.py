import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "collect_openalex_candidates.py"
spec = importlib.util.spec_from_file_location("collector", MODULE_PATH)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


def test_abstract_reconstruction_respects_word_positions():
    index = {"beta": [1], "alpha": [0], "again": [2, 3]}
    assert collector.reconstruct_abstract(index) == "alpha beta again again"


def test_doi_and_title_normalization():
    assert collector.normalize_doi("https://doi.org/10.1000/ABC.") == "10.1000/abc"
    assert collector.normalize_title("A Study: AI & Literature!") == "a study ai literature"


def test_duplicate_cluster_uses_exact_doi_or_title_year_author():
    rows = [
        {"openalex_id": "W1", "doi": "10.1/ABC", "title": "Paper", "year": 2020,
         "first_author_openalex_id": "A1"},
        {"openalex_id": "W2", "doi": "https://doi.org/10.1/abc", "title": "Paper v2", "year": 2021,
         "first_author_openalex_id": "A2"},
        {"openalex_id": "W3", "doi": "", "title": "Same title", "year": 2022,
         "first_author_openalex_id": "A3"},
        {"openalex_id": "W4", "doi": "", "title": "Same title", "year": 2022,
         "first_author_openalex_id": "A3"},
    ]
    result = collector.assign_duplicate_clusters(rows)
    assert result[0]["duplicate_cluster_id"] == result[1]["duplicate_cluster_id"]
    assert result[2]["duplicate_cluster_id"] == result[3]["duplicate_cluster_id"]
    assert result[0]["duplicate_review_status"] == "needs_canonical_review"
    assert result[2]["duplicate_review_status"] == "needs_canonical_review"


def test_search_task_set_covers_all_year_bands_and_routes():
    seeds = [{"doi": "10.1000/seed"}]
    tasks = collector.build_tasks(50, seeds)
    ids = {task["route_id"] for task in tasks}
    assert any(x.startswith("Q01_automated_literature_screening") for x in ids)
    assert any(x.startswith("T01_information_retrieval") for x in ids)
    assert any(x.startswith("SEED01_resolve") for x in ids)
    assert len([x for x in ids if "_2015_2016" in x]) >= 12
