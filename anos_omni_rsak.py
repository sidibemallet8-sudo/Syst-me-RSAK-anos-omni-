
"""ANOS OMNI — RSAK V1
Réorganisation Structurelle Adaptative des Connaissances.
Prototype expérimental autonome, sans dépendance externe.
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

        conclusions = {r.conclusion for r in matched}

        if len(conclusions) > 1:
            return {
                "status": "CONFLICT",
                "answer": None
            }

        return {
            "status": "ANSWER",
            "answer": matched[0].conclusion,
            "rules": [r.id for r in matched]
        }

    def propose_reorganization(self, rule_id):
        rule = self.rules[rule_id]

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
            groups = {}

            for ex in relevant:
                attrs = ex["attributes"]

                if key not in attrs:
                    continue

                value = str(attrs[key])
                groups.setdefault(value, set()).add(
                    ex["conclusion"]
                )

            if len(groups) < 2:
                continue

            if not all(len(values) == 1
                       for values in groups.values()):
                continue

            self.counter += 1
            proposal_id = f"P{self.counter:03d}"

            children = []

            for ex in relevant:
                value = ex["attributes"].get(key)

                child = {
                    "conditions": {
                        **rule.conditions,
                        key: value
                    },
                    "conclusion": ex["conclusion"]
                }

                if child not in children:
                    children.append(child)

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

    # 1. Initial knowledge
    rule = ai.add_rule(
        {"wheels": 4},
        "motorized"
    )

    print("\nInitial rule:", rule)

    # 2. Supporting example
    ai.add_example(
        {"wheels": 4, "engine": True},
        "motorized"
    )

    # 3. Counterexample
    conflicts = ai.add_example(
        {"wheels": 4, "engine": False},
        "not_motorized"
    )

    print("\nDetected counterexamples:", conflicts)

    # 4. Reorganization proposal
    proposal = ai.propose_reorganization(rule)

    print("\nReorganization proposal:")
    print(json.dumps(proposal, indent=2))

    # 5. Human validation
    if proposal:
        print("\nHuman validation: APPROVED")

        ai.validate(proposal["id"], True)

    # 6. New queries
    print("\nQuery: four wheels, engine present")

    print(ai.query({
        "wheels": 4,
        "engine": True
    }))

    print("\nQuery: four wheels, engine absent")

    print(ai.query({
        "wheels": 4,
        "engine": False
    }))

    print("\nQuery: four wheels, engine unknown")

    print(ai.query({
        "wheels": 4
    }))

    # 7. Save memory
    ai.save()

    print("\nMemory saved.")
    print("=== DEMONSTRATION COMPLETE ===")


if __name__ == "__main__":
    demonstration()
