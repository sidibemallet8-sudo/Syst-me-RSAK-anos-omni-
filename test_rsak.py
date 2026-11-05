import json
import tempfile
import unittest
from pathlib import Path

from anos_omni_rsak import AnosOmniRSAK


class TestAnosOmniRSAK(unittest.TestCase):
    def setUp(self):
        self.ai = AnosOmniRSAK()

    def prepare_conflict(self):
        rule = self.ai.add_rule({"wheels": 4}, "motorized")
        self.ai.add_example({"wheels": 4, "engine": True}, "motorized")
        self.ai.add_example({"wheels": 4, "engine": False}, "not_motorized")
        return rule

    def test_rule_creation_and_counterexample_detection(self):
        rule = self.prepare_conflict()
        events = [event for event in self.ai.history
                  if event["event"] == "EXAMPLE_LEARNED"]
        self.assertIn(rule, events[-1]["details"]["conflicts"])

    def test_reorganization_is_explainable_and_applies_after_approval(self):
        rule = self.prepare_conflict()
        proposal = self.ai.propose_reorganization(rule)
        self.assertIsNotNone(proposal)
        self.assertEqual(proposal["attribute"], "engine")
        self.assertIn("not proof", proposal["explanation"])
        self.assertGreater(proposal["heuristic_score"], 0)
        self.ai.validate(proposal["id"], True)
        self.assertEqual(self.ai.rules[rule].status, "archived")
        result = self.ai.query({"wheels": 4, "engine": False})
        self.assertEqual((result["status"], result["answer"]),
                         ("ANSWER", "not_motorized"))

    def test_abstention_and_conflict(self):
        self.ai.add_rule({"wheels": 4, "engine": True}, "motorized")
        self.assertEqual(self.ai.query({"wheels": 4})["status"], "ABSTENTION")
        self.ai.add_rule({"wheels": 4}, "not_motorized")
        self.assertEqual(self.ai.query({"wheels": 4, "engine": True})["status"],
                         "CONFLICT")

    def test_rejected_proposal_keeps_parent_active(self):
        rule = self.prepare_conflict()
        proposal = self.ai.propose_reorganization(rule)
        self.ai.validate(proposal["id"], False)
        self.assertEqual(self.ai.rules[rule].status, "active")

    def test_multiple_candidates_are_ranked_deterministically(self):
        rule = self.ai.add_rule({"object": "vehicle"}, "powered")
        self.ai.add_example({"object": "vehicle", "engine": True,
                             "fuel": "electric"}, "powered")
        self.ai.add_example({"object": "vehicle", "engine": False,
                             "fuel": "none"}, "unpowered")
        proposals = self.ai.propose_reorganizations(rule)
        self.assertEqual(len(proposals), 2)
        self.assertGreaterEqual(proposals[0]["heuristic_score"],
                                proposals[1]["heuristic_score"])

    def test_missing_attribute_or_mixed_group_blocks_candidate(self):
        rule = self.prepare_conflict()
        self.ai.add_example({"wheels": 4}, "unknown")
        self.assertIsNone(self.ai.propose_reorganization(rule))

    def test_invalid_inputs_and_unknown_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            self.ai.add_rule({}, "answer")
        with self.assertRaises(ValueError):
            self.ai.add_example({"x": 1}, " ")
        with self.assertRaises(ValueError):
            self.ai.validate("missing", True)

    def test_snapshot_round_trip(self):
        self.prepare_conflict()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            self.ai.save(path)
            restored = AnosOmniRSAK.load(path)
        self.assertEqual(restored.state(), self.ai.state())
        self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["schema_version"], 2)


if __name__ == "__main__":
    unittest.main()
