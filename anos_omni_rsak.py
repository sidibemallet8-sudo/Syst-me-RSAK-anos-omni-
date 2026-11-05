"""ANOS OMNI — RSAK V2 experimental rule-revision engine.

RSAK is a small, explainable symbolic prototype. It is not a language model,
robot controller, or a scientifically validated replacement for existing AI.
"""

from dataclasses import asdict, dataclass
import json
import math
import os
from pathlib import Path
from typing import Any


@dataclass
class Rule:
    id: str
    conditions: dict[str, Any]
    conclusion: str
    status: str = "active"
    parent: str | None = None


class AnosOmniRSAK:
    """Manage rules, evidence, conflicts, and human-reviewed revisions."""

    SCHEMA_VERSION = 2

    def __init__(self):
        self.rules: dict[str, Rule] = {}
        self.examples: list[dict[str, Any]] = []
        self.proposals: dict[str, dict[str, Any]] = {}
        self.history: list[dict[str, Any]] = []
        self.counter = 0
        self.example_counter = 0

    @staticmethod
    def _validate_json(value: Any, label: str) -> None:
        try:
            json.dumps(value, ensure_ascii=False, allow_nan=False)
        except (TypeError, ValueError) as error:
            raise ValueError(f"{label} must contain JSON-compatible values") from error

    @staticmethod
    def _validate_conditions(conditions: dict[str, Any]) -> None:
        if not isinstance(conditions, dict):
            raise ValueError("Conditions must be a dictionary")
        AnosOmniRSAK._validate_json(conditions, "Conditions")

    @staticmethod
    def _validate_conclusion(conclusion: str) -> None:
        if not isinstance(conclusion, str) or not conclusion.strip():
            raise ValueError("Conclusion must be a non-empty string")

    def log(self, event: str, details: Any) -> None:
        self.history.append({"event": event, "details": details})

    def add_rule(self, conditions: dict[str, Any], conclusion: str) -> str:
        self._validate_conditions(conditions)
        self._validate_conclusion(conclusion)
        self.counter += 1
        rule_id = f"R{self.counter:03d}"
        self.rules[rule_id] = Rule(rule_id, dict(conditions), conclusion)
        self.log("RULE_CREATED", rule_id)
        return rule_id

    def add_example(self, attributes: dict[str, Any], conclusion: str) -> list[str]:
        self._validate_conditions(attributes)
        self._validate_conclusion(conclusion)
        self.example_counter += 1
        example = {
            "id": f"E{self.example_counter:03d}",
            "attributes": dict(attributes),
            "conclusion": conclusion,
        }
        self.examples.append(example)

        conflicts = [
            rule.id
            for rule in self.rules.values()
            if rule.status == "active"
            and self.matches(rule, attributes)
            and rule.conclusion != conclusion
        ]
        self.log("EXAMPLE_LEARNED", {"example": example, "conflicts": conflicts})
        return conflicts

    @staticmethod
    def matches(rule: Rule, attributes: dict[str, Any]) -> bool:
        return all(key in attributes and attributes[key] == value
                   for key, value in rule.conditions.items())

    def query(self, attributes: dict[str, Any]) -> dict[str, Any]:
        self._validate_conditions(attributes)
        matched = [
            rule for rule in self.rules.values()
            if rule.status == "active" and self.matches(rule, attributes)
        ]
        if not matched:
            return {
                "status": "ABSTENTION",
                "answer": None,
                "reason": "Insufficient knowledge: no active rule matches",
            }

        # More specific rules take precedence; conflicts at the same specificity
        # remain explicit rather than being resolved arbitrarily.
        specificity = max(len(rule.conditions) for rule in matched)
        best = [rule for rule in matched if len(rule.conditions) == specificity]
        conclusions = {rule.conclusion for rule in best}
        if len(conclusions) != 1:
            return {
                "status": "CONFLICT",
                "answer": None,
                "rules": [rule.id for rule in best],
                "reason": "Equally specific active rules disagree",
            }

        answer = best[0].conclusion
        evidence = [
            example for example in self.examples
            if example["conclusion"] == answer
            and any(self.matches(rule, example["attributes"]) for rule in best)
        ]
        return {
            "status": "ANSWER",
            "answer": answer,
            "rules": [rule.id for rule in best],
            "specificity": specificity,
            "supporting_examples": [example["id"] for example in evidence],
            "explanation": "Answer derived from the most specific matching active rule(s).",
        }

    @staticmethod
    def _entropy(labels: list[str]) -> float:
        if not labels:
            return 0.0
        counts: dict[str, int] = {}
        for label in labels:
            counts[label] = counts.get(label, 0) + 1
        total = len(labels)
        return -sum((count / total) * math.log2(count / total)
                    for count in counts.values())

    @staticmethod
    def _value_key(value: Any) -> str:
        # Include the type so that True and 1 are not merged as equal groups.
        return json.dumps({"type": type(value).__name__, "value": value},
                          sort_keys=True, ensure_ascii=False, allow_nan=False)

    def propose_reorganization(self, rule_id: str) -> dict[str, Any] | None:
        if rule_id not in self.rules:
            raise ValueError(f"Unknown rule: {rule_id}")
        rule = self.rules[rule_id]
        if rule.status != "active":
            return None

        relevant = [example for example in self.examples
                    if self.matches(rule, example["attributes"])]
        labels = [example["conclusion"] for example in relevant]
        if len(set(labels)) < 2:
            return None

        candidates = []
        for key in sorted({key for example in relevant
                           for key in example["attributes"]}):
            # Missing values are not silently treated as a category: they make
            # this candidate incomplete and reduce its coverage.
            covered = [example for example in relevant if key in example["attributes"]]
            coverage = len(covered) / len(relevant)
            groups: dict[str, dict[str, Any]] = {}
            for example in covered:
                value = example["attributes"][key]
                value_key = self._value_key(value)
                group = groups.setdefault(value_key, {"value": value, "examples": []})
                group["examples"].append(example)

            if len(groups) < 2:
                continue
            if any(len({ex["conclusion"] for ex in group["examples"]}) != 1
                   for group in groups.values()):
                continue

            parent_entropy = self._entropy([ex["conclusion"] for ex in covered])
            total = len(covered)
            child_entropy = sum(
                (len(group["examples"]) / total)
                * self._entropy([ex["conclusion"] for ex in group["examples"]])
                for group in groups.values()
            )
            gain = max(0.0, parent_entropy - child_entropy)
            candidates.append({
                "attribute": key,
                "information_gain": round(gain, 6),
                "coverage": round(coverage, 6),
                "score": round(gain * coverage, 6),
                "groups": [
                    {
                        "value": group["value"],
                        "conclusion": group["examples"][0]["conclusion"],
                        "support": len(group["examples"]),
                    }
                    for group in groups.values()
                ],
            })

        if not candidates:
            return None
        candidates.sort(key=lambda item: (-item["score"], item["attribute"]))
        selected = candidates[0]
        children = [
            {
                "conditions": {**rule.conditions, selected["attribute"]: group["value"]},
                "conclusion": group["conclusion"],
            }
            for group in selected["groups"]
        ]

        self.counter += 1
        proposal_id = f"P{self.counter:03d}"
        proposal = {
            "id": proposal_id,
            "parent": rule_id,
            "attribute": selected["attribute"],
            "children": children,
            "candidates": candidates,
            "status": "PENDING",
            "evidence": [example["id"] for example in relevant],
            "method": "maximum empirical information gain multiplied by coverage",
            "warning": "Candidate ranking is heuristic; validate on independent data before use.",
        }
        self.proposals[proposal_id] = proposal
        self.log("REORGANIZATION_PROPOSED", proposal)
        return proposal

    def validate(self, proposal_id: str, approved: bool) -> dict[str, Any]:
        if proposal_id not in self.proposals:
            raise ValueError(f"Unknown proposal: {proposal_id}")
        if not isinstance(approved, bool):
            raise ValueError("Approval must be a boolean")
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
                    conditions=dict(child["conditions"]),
                    conclusion=child["conclusion"],
                    parent=parent.id,
                )
            proposal["status"] = "APPROVED"
        else:
            proposal["status"] = "REJECTED"

        self.log("HUMAN_VALIDATION", {"proposal": proposal_id, "approved": approved})
        return proposal

    def state(self) -> dict[str, Any]:
        return {
            "schema_version": self.SCHEMA_VERSION,
            "rules": [asdict(rule) for rule in self.rules.values()],
            "examples": self.examples,
            "proposals": self.proposals,
            "history": self.history,
            "counter": self.counter,
            "example_counter": self.example_counter,
        }

    def save(self, filename: str | os.PathLike = "anos_memory.json") -> None:
        """Atomically save a JSON snapshot to reduce partial-file corruption."""
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(self.state(), file, ensure_ascii=False, indent=2, allow_nan=False)
            file.flush()
            os.fsync(file.fileno())
        temporary.replace(path)

    @classmethod
    def load(cls, filename: str | os.PathLike) -> "AnosOmniRSAK":
        """Load a snapshot; accepts the earlier V1 state shape as well."""
        with Path(filename).open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError("Memory file must contain a JSON object")
        version = data.get("schema_version", 1)
        if version not in (1, cls.SCHEMA_VERSION):
            raise ValueError(f"Unsupported memory schema version: {version}")

        engine = cls()
        for item in data.get("rules", []):
            rule = Rule(**item)
            engine.rules[rule.id] = rule
        engine.examples = data.get("examples", [])
        engine.proposals = data.get("proposals", {})
        engine.history = data.get("history", [])
        engine.counter = data.get("counter", max(
            (int(rule_id[1:]) for rule_id in engine.rules if rule_id[1:].isdigit()),
            default=0,
        ))
        engine.example_counter = data.get("example_counter", len(engine.examples))
        return engine


def demonstration() -> None:
    ai = AnosOmniRSAK()
    print("ANOS OMNI — RSAK V2 | démonstration expérimentale")
    rule_id = ai.add_rule({"wheels": 4}, "motorized")
    ai.add_example({"wheels": 4, "engine": True}, "motorized")
    conflicts = ai.add_example({"wheels": 4, "engine": False}, "not_motorized")
    print("Contre-exemple détecté contre :", conflicts)

    proposal = ai.propose_reorganization(rule_id)
    print("Proposition classée par gain d'information :")
    print(json.dumps(proposal, indent=2, ensure_ascii=False))
    if proposal:
        print("Validation humaine simulée : APPROVED")
        ai.validate(proposal["id"], True)

    for attributes in (
        {"wheels": 4, "engine": True},
        {"wheels": 4, "engine": False},
        {"wheels": 4},
    ):
        print("Requête", attributes, "→", ai.query(attributes))


if __name__ == "__main__":
    demonstration()
