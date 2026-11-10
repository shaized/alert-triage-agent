import copy
import json
from pathlib import Path
import unittest

from agent import analyze


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path(__file__).with_name("example.json").read_text())

    def test_queue_preserves_highest_source_priority_and_gaps(self):
        row = analyze(self.data)["findings"][0]
        self.assertEqual(row["source_priority"], "high")
        self.assertEqual(row["alerts_without_evidence"], ["alert-2"])
        self.assertEqual(row["status"], "analyst_review_required")

    def test_distinct_entities_stay_separate(self):
        self.data["alerts"][1]["entity"] = "lab/another-account"
        self.assertEqual(len(analyze(self.data)["findings"]), 2)

    def test_unknown_evidence_is_rejected(self):
        self.data["alerts"][0]["evidence_ids"] = ["missing"]
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_timestamp_extrema_are_not_lexical(self):
        self.data["alerts"][0]["timestamp"] = "2026-01-15T10:00:00.1Z"
        self.data["alerts"][1]["timestamp"] = "2026-01-15T12:00:00+02:00"
        row = analyze(self.data)["findings"][0]
        self.assertEqual(row["first_seen"], "2026-01-15T10:00:00Z")
        self.assertEqual(row["last_seen"], "2026-01-15T10:00:00.100000Z")

    def test_duplicate_alerts_are_rejected(self):
        self.data["alerts"].append(copy.deepcopy(self.data["alerts"][0]))
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_empty_queue_does_not_close_anything(self):
        self.data["alerts"] = []
        self.assertEqual(analyze(self.data)["summary"]["automatic_dispositions"], 0)


if __name__ == "__main__":
    unittest.main()
