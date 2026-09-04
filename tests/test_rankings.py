import unittest
from pathlib import Path

import rankings


def control(status="documented", source_url="https://example.com/policy"):
    return {"status": status, "source_url": source_url, "note": "Synthetic test evidence."}


def fixture():
    controls_a = {name: control() for name in rankings.CONTROLS}
    controls_b = {name: control() for name in rankings.CONTROLS}
    controls_b["retention_period"] = control("not_documented", "")
    return {
        "schema_version": 1,
        "id": "test-security-ranking",
        "title": "Comparable test",
        "reviewed_at": "2026-09-04",
        "author": {"github": "tester", "affiliation": "Independent"},
        "conflicts": [],
        "methodology_url": "https://example.com/method",
        "entries": [
            {"provider": "B", "service_scope": "API", "controls": controls_b},
            {"provider": "A", "service_scope": "API", "controls": controls_a},
        ],
    }


class RankingTests(unittest.TestCase):
    def test_ranks_documentation_coverage(self):
        data = rankings.validate(fixture(), Path("example.json"))
        self.assertEqual([item["provider"] for item in data["entries"]], ["A", "B"])
        self.assertEqual(data["entries"][0]["transparency_score"], 100)

    def test_documented_control_requires_source(self):
        data = fixture()
        data["entries"][0]["controls"]["privacy_policy"]["source_url"] = ""
        with self.assertRaises(ValueError):
            rankings.validate(data, Path("example.json"))

    def test_requires_all_controls(self):
        data = fixture()
        del data["entries"][0]["controls"]["training_use"]
        with self.assertRaises(ValueError):
            rankings.validate(data, Path("example.json"))

    def test_empty_ranking_states_evidence_limit(self):
        self.assertIn("No real provider is ranked yet", rankings.render([]))


if __name__ == "__main__":
    unittest.main()
