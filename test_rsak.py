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

    def test_rule_creation_and_input_validation(self):
        rule = self.ai.add_rule({"wheels": 4}, "motorized")
        self.assertIn(rule, self.ai.rules)
        with self.assertRaises(ValueError):
            self.ai.add_rule([], "invalid")
        with self.assertRaises(ValueError):
            self.ai.add_example({}, "")

    def test_counterexample_detection(self):
        rule = self.prepare_conflict()
        events = [event for event in self.ai.history if event["event"] == "EXAMPLE_LEARNED"]
        self.assertIn(rule, events[-1]["details"]["conflicts"])

    def test_reorganization_has_ranked_explanation(self):
        rule = self.prepare_conflict()
        proposal = self.ai.propose_reorganization(rule)
        self.assertIsNotNone(proposal)
        self.assertEqual(proposal["attribute"], "engine")
        self.assertGreater(proposal["candidates"][0]["information_gain"], 0)
        self.assertEqual(proposal["status"], "PENDING")

    def test_approved_reorganization_and_specific_rule_query(self):
        rule = self.prepare_conflict()
        proposal = self.ai.propose_reorganization(rule)
        self.ai.validate(proposal["id"], True)
        self.assertEqual(self.ai.rules[rule].status, "archived")
        result = self.ai.query({"wheels": 4, "engine": False})
        self.assertEqual(result["status"], "ANSWER")
        self.assertEqual(result["answer"], "not_motorized")
        self.assertIn("explanation", result)

    def test_abstention_and_equal_specificity_conflict(self):
        self.ai.add_rule({"engine": True}, "running")
        self.assertEqual(self.ai.query({"wheels": 4})["status"], "ABSTENTION")
        self.ai.add_rule({"engine": True}, "stopped")
        self.assertEqual(self.ai.query({"engine": True})["status"], "CONFLICT")

    def test_rejected_proposal_keeps_parent_active(self):
        rule = self.prepare_conflict()
        proposal = self.ai.propose_reorganization(rule)
        self.ai.validate(proposal["id"], False)
        self.assertEqual(self.ai.rules[rule].status, "active")

    def test_missing_attributes_are_not_used_as_split(self):
        rule = self.prepare_conflict()
        self.ai.add_example({"wheels": 4}, "unknown")
        self.assertIsNone(self.ai.propose_reorganization(rule))

    def test_unknown_or_reprocessed_proposals_fail_clearly(self):
        with self.assertRaisesRegex(ValueError, "Unknown proposal"):
            self.ai.validate("P999", True)
        rule = self.prepare_conflict()
        proposal = self.ai.propose_reorganization(rule)
        self.ai.validate(proposal["id"], False)
        with self.assertRaisesRegex(ValueError, "already processed"):
            self.ai.validate(proposal["id"], True)

    def test_save_and_load_round_trip(self):
        self.prepare_conflict()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            self.ai.save(path)
            restored = AnosOmniRSAK.load(path)
        self.assertEqual(restored.state(), self.ai.state())
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}, {})


if __name__ == "__main__":
    unittest.main()
