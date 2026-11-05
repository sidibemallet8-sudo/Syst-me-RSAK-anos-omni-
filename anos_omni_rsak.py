
"""ANOS OMNI — RSAK V1
Réorganisation Structurelle Adaptative des Connaissances.
Prototype expérimental autonome.
"""

from dataclasses import dataclass, asdict
import json


@dataclass
class Rule:
    id: str
    conditions: dict
    conclusion: str
    status: str = "active"
    parent: str = None


class AnosOmniRSAK:

    def __init__(self):
        self.rules = {}
        self.examples = []
        self.proposals = {}
        self.history = []
        self.counter = 0

    def log(self, event, details):
        self.history.append({
            "event": event,
            "details": details
        })

    def add_rule(self, conditions, conclusion):
        self.counter += 1
        rule_id = f"R{self.counter:03d}"

        self.rules[rule_id] = Rule(
            rule_id, conditions, conclusion
        )

        self.log("RULE_CREATED", rule_id)
        return rule_id

    def add_example(self, attributes, conclusion):
        example = {
            "attributes": attributes,
            "conclusion": conclusion
        }

        self.examples.append(example)
        conflicts = []

        for rule in self.rules.values():
            if rule.status != "active":
                continue

            if self.matches(rule, attributes):
                if rule.conclusion != conclusion:
                    conflicts.append(rule.id)

        self.log("EXAMPLE_LEARNED", {
            "example": example,
            "conflicts": conflicts
        })

        return conflicts

    @staticmethod
    def matches(rule, attributes):
        return all(
            key in attributes and attributes[key] == value
            for key, value in rule.conditions.items()
        )

    def query(self, attributes):
        matched = [
            rule for rule in self.rules.values()
            if rule.status == "active"
            and self.matches(rule, attributes)
        ]

        if not matched:
            return {
                "status": "ABSTENTION",
                "answer": None,
                "reason": "Insufficient knowledge"
            }

        conclusions = {rule.conclusion for rule in matched}

        if len(conclusions) > 1:
            return {
                "status": "CONFLICT",
                "answer": None
            }

        return {
            "status": "ANSWER",
            "answer": matched[0].conclusion,
            "rules": [rule.id for rule in matched]
        }

    def propose_reorganization(self, rule_id):
        rule = self.rules[rule_id]

        if rule.status != "active":
            return None

        relevant = [
            ex for ex in self.examples
            if self.matches(rule, ex["attributes"])
        ]

        labels = {ex["conclusion"] for ex in relevant}

        if len(labels) < 2:
            return None

        keys = set()

        for ex in relevant:
            keys.update(ex["attributes"].keys())

        for key in sorted(keys):

            # Tous les exemples doivent posséder cet attribut.
            if not all(key in ex["attributes"] for ex in relevant):
                continue

            groups = {}

            for ex in relevant:
                value = ex["attributes"][key]

                value_id = json.dumps(
                    {
                        "type": type(value).__name__,
                        "value": value
                    },
                    sort_keys=True,
                    ensure_ascii=False
                )

                if value_id not in groups:
                    groups[value_id] = {
                        "value": value,
                        "conclusions": set()
                    }

                groups[value_id]["conclusions"].add(
                    ex["conclusion"]
                )

            if len(groups) < 2:
                continue

            if not all(
                len(group["conclusions"]) == 1
                for group in groups.values()
            ):
                continue

            children = []

            for group in groups.values():
                children.append({
                    "conditions": {
                        **rule.conditions,
                        key: group["value"]
                    },
                    "conclusion": next(iter(group["conclusions"]))
                })

            self.counter += 1
            proposal_id = f"P{self.counter:03d}"

            proposal = {
                "id": proposal_id,
                "parent": rule_id,
                "attribute": key,
                "children": children,
                "status": "PENDING"
            }

            self.proposals[proposal_id] = proposal
            self.log("REORGANIZATION_PROPOSED", proposal)

            return proposal

        return None

    def validate(self, proposal_id, approved):
        proposal = self.proposals[proposal_id]

        if proposal["status"] != "PENDING":
            raise ValueError("Proposal already processed")

        if approved:
            parent = self.rules[proposal["parent"]]
            parent.status = "archived"

            for child in proposal["children"]:
                self.counter += 1
                rule_id = f"R{self.counter:03d}"

                self.rules[rule_id] = Rule(
                    id=rule_id,
                    conditions=child["conditions"],
                    conclusion=child["conclusion"],
                    parent=parent.id
                )

            proposal["status"] = "APPROVED"
        else:
            proposal["status"] = "REJECTED"

        self.log("HUMAN_VALIDATION", {
            "proposal": proposal_id,
            "approved": approved
        })

        return proposal

    def state(self):
        return {
            "rules": [
                asdict(rule)
                for rule in self.rules.values()
            ],
            "examples": self.examples,
            "proposals": self.proposals,
            "history": self.history
        }

    def save(self, filename="anos_memory.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                self.state(),
                file,
                ensure_ascii=False,
                indent=2
            )


def demonstration():
    ai = AnosOmniRSAK()

    print("\n=== ANOS OMNI RSAK V1 ===")

    rule = ai.add_rule({"wheels": 4}, "motorized")

    ai.add_example(
        {"wheels": 4, "engine": True},
        "motorized"
    )

    conflicts = ai.add_example(
        {"wheels": 4, "engine": False},
        "not_motorized"
    )

    print("\nContradictions détectées :", conflicts)

    proposal = ai.propose_reorganization(rule)

    print("\nProposition :")
    print(json.dumps(proposal, indent=2, ensure_ascii=False))

    if proposal:
        print("\nValidation simulée : APPROVED")
        ai.validate(proposal["id"], True)

    print("\nMoteur présent :")
    print(ai.query({"wheels": 4, "engine": True}))

    print("\nMoteur absent :")
    print(ai.query({"wheels": 4, "engine": False}))

    print("\nMoteur inconnu :")
    print(ai.query({"wheels": 4}))

    ai.save()

    print("\nMémoire sauvegardée.")
    print("=== DÉMONSTRATION TERMINÉE ===")


if __name__ == "__main__":
    demonstration()
