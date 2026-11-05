
import unittest

from anos_omni_rsak import AnosOmniRSAK


class TestAnosOmniRSAK(unittest.TestCase):

    def setUp(self):
        self.ai = AnosOmniRSAK()

    def prepare_conflict(self):
        rule = self.ai.add_rule(
            {"wheels": 4},
            "motorized"
        )

        self.ai.add_example(
            {"wheels": 4, "engine": True},
            "motorized"
        )

        self.ai.add_example(
            {"wheels": 4, "engine": False},
            "not_motorized"
        )

        return rule

    def test_rule_creation(self):
        rule = self.ai.add_rule(
            {"wheels": 4},
            "motorized"
        )

        self.assertIn(rule, self.ai.rules)

    def test_counterexample_detection(self):
        rule = self.prepare_conflict()

        conflicts = [
            event["details"]["conflicts"]
            for event in self.ai.history
            if event["event"] == "EXAMPLE_LEARNED"
        ]

        self.assertIn(rule, conflicts[-1])

    def test_reorganization_and_validation(self):
        rule = self.prepare_conflict()

        proposal = self.ai.propose_reorganization(rule)

        self.assertIsNotNone(proposal)

        self.ai.validate(proposal["id"], True)

        self.assertEqual(
            self.ai.rules[rule].status,
            "archived"
        )

    def test_unknown_information(self):
        self.ai.add_rule(
            {"wheels": 4, "engine": True},
            "motorized"
        )

        result = self.ai.query({"wheels": 4})

        self.assertEqual(result["status"], "ABSTENTION")

    def test_rejected_proposal(self):
        rule = self.prepare_conflict()

        proposal = self.ai.propose_reorganization(rule)

        self.ai.validate(proposal["id"], False)

        self.assertEqual(
            self.ai.rules[rule].status,
            "active"
        )

    def test_missing_attribute_blocks_reorganization(self):
        rule = self.prepare_conflict()

        self.ai.add_example(
            {"wheels": 4},
            "unknown"
        )

        proposal = self.ai.propose_reorganization(rule)

        self.assertIsNone(proposal)

    def test_query_after_approved_reorganization(self):
        rule = self.prepare_conflict()

        proposal = self.ai.propose_reorganization(rule)
        self.ai.validate(proposal["id"], True)

        result = self.ai.query({
            "wheels": 4,
            "engine": False
        })

        self.assertEqual(result["status"], "ANSWER")
        self.assertEqual(result["answer"], "not_motorized")


if __name__ == "__main__":
    unittest.main()
