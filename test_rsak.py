
import unittest

from anos_omni_rsak import AnosOmniRSAK


class TestAnosOmniRSAK(unittest.TestCase):

    def setUp(self):
        self.ai = AnosOmniRSAK()

    def test_rule_creation(self):
        rule = self.ai.add_rule(
            {"wheels": 4},
            "motorized"
        )
        self.assertIn(rule, self.ai.rules)

    def test_counterexample_detection(self):
        rule = self.ai.add_rule(
            {"wheels": 4},
            "motorized"
        )

        self.ai.add_example(
            {"wheels": 4, "engine": True},
            "motorized"
        )

        conflicts = self.ai.add_example(
            {"wheels": 4, "engine": False},
            "not_motorized"
        )

        self.assertIn(rule, conflicts)

    def test_reorganization_and_validation(self):
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

        proposal = self.ai.propose_reorganization(rule)

        self.ai.validate(proposal["id"], False)

        self.assertEqual(
            self.ai.rules[rule].status,
            "active"
        )


if __name__ == "__main__":
    unittest.main()
