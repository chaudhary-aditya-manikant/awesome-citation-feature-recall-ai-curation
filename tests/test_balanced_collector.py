from pathlib import Path
import importlib.util

MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "collect_openalex_candidates_balanced.py"
spec = importlib.util.spec_from_file_location("balanced_collector", MODULE_PATH)
collector = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(collector)


def test_all_search_and_topic_exact_year_routes_are_generated():
    tasks = collector.build_route_tasks(20, 20261031)
    assert len(tasks) == 132
    assert sum(t["route_family"] == "search" for t in tasks) == 88
    assert sum(t["route_family"] == "topic" for t in tasks) == 44
    for task in tasks:
        params = task["params"]
        assert params["sample"] == params["per_page"] == 20
        assert isinstance(params["seed"], int)
        assert "sort" not in params


def test_exact_years_cover_2015_through_2025():
    tasks = collector.build_route_tasks(20, 20261031)
    years = {int(t["route_id"].rsplit("_", 1)[1]) for t in tasks}
    assert years == set(range(2015, 2026))


def test_route_seeds_are_stable_and_distinct():
    a = collector.stable_seed("Q01_route_2015", 20261031)
    b = collector.stable_seed("Q01_route_2015", 20261031)
    c = collector.stable_seed("Q01_route_2016", 20261031)
    assert a == b and a != c


def test_collection_maximum_fits_frozen_cap():
    assert collector.expected_max_records(20, 30, 5) == 2965
    assert collector.expected_max_records(20, 30, 5) <= 3000
    assert collector.expected_max_records(21, 30, 5) > 3000


def test_citation_neighbourhoods_are_sampled_without_sorting():
    seeds = [("SEED01", "https://openalex.org/W123"), ("SEED02", "https://openalex.org/W456")]
    tasks = collector.build_citation_tasks(seeds, 30, 20261031)
    assert len(tasks) == 4
    for task in tasks:
        assert task["route_family"] == "citation_neighbourhood"
        assert task["params"]["sample"] == task["params"]["per_page"] == 30
        assert "sort" not in task["params"]


def test_different_same_title_publications_with_different_abstracts_stay_separate():
    rows = [
        {"openalex_id": "W1", "doi": "10.1/a", "title": "A perspectival mirror", "year": 2024,
         "author_openalex_ids": "A1|A2", "abstract": "First publication about an elephant metaphor."},
        {"openalex_id": "W2", "doi": "10.1/b", "title": "A perspectival mirror", "year": 2024,
         "author_openalex_ids": "A1|A2", "abstract": "Second article with a materially different discussion and conclusion."},
    ]
    result = collector.assign_duplicate_clusters(rows)
    assert result[0]["duplicate_cluster_id"] != result[1]["duplicate_cluster_id"]


def test_same_paper_with_author_order_reversed_is_clustered():
    rows = [
        {"openalex_id": "W3", "doi": "10.1/c", "title": "Natural language generation", "year": 2023,
         "author_openalex_ids": "A1|A2", "abstract": "A study proposes a method for data augmentation and text generation."},
        {"openalex_id": "W4", "doi": "10.1/d", "title": "Natural language generation", "year": 2023,
         "author_openalex_ids": "A2|A1", "abstract": "A study proposes a method for data augmentation and text generation."},
    ]
    result = collector.assign_duplicate_clusters(rows)
    assert result[0]["duplicate_cluster_id"] == result[1]["duplicate_cluster_id"]


def test_known_manual_duplicate_group_is_preserved(tmp_path):
    group_file = tmp_path / "known_duplicate_groups.csv"
    group_file.write_text(
        "duplicate_group_id,openalex_id,review_status\n"
        "MANUAL_G,https://openalex.org/W5,pending_source_check\n"
        "MANUAL_G,https://openalex.org/W6,pending_source_check\n",
        encoding="utf-8",
    )
    rows = [
        {"openalex_id": "https://openalex.org/W5", "doi": "", "title": "A", "year": 2020, "author_openalex_ids": "A1", "abstract": "one"},
        {"openalex_id": "https://openalex.org/W6", "doi": "", "title": "B", "year": 2021, "author_openalex_ids": "A2", "abstract": "two"},
    ]
    result = collector.assign_duplicate_clusters(rows, group_file)
    assert result[0]["duplicate_cluster_id"] == "MANUAL_G"
    assert result[1]["duplicate_cluster_id"] == "MANUAL_G"
