"""ANOS OMNI — RSAK V2 experimental knowledge-revision engine.

RSAK is a deterministic rule-based research prototype. Its heuristic scores are
ranking aids, not probabilities, confidence estimates, or evidence of accuracy.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import tempfile
from typing import Any


SCHEMA_VERSION = 2


@dataclass
class Rule:
    id: str
    conditions: dict[str, Any]
    conclusion: str
    status: str = "active"
    parent: str | None = None


class AnosOmniRSAK:
    """Small, explainable rule engine with human-reviewed revision proposals."""

    def __init__(self) -> None:
        self.rules: dict[str, Rule] = {}
        self.examples: list[dict[str, Any]] = []
        self.proposals: dict[str, dict[str, Any]] = {}
        self.history: list[dict[str, Any]] = []
        self.counter = 0

    def log(self, event: str, details: Any) -> None:
        self.history.append({"event": event, "details": deepcopy(details)})

    @staticmethod
    def _validate_conditions(conditions: Any) -> dict[str, Any]:
        if not isinstance(conditions, dict) or not conditions:
            raise ValueError("Conditions must be a non-empty object")
        if not all(isinstance(key, str) and key for key in conditions):
            raise ValueError("Condition names must be non-empty strings")
        try:
            json.dumps(conditions, ensure_ascii=False, allow_nan=False)
        except (TypeError, ValueError) as error:
            raise ValueError("Conditions must contain finite JSON values") from error
        return deepcopy(conditions)

    @staticmethod
    def _validate_conclusion(conclusion: Any) -> str:
        if not isinstance(conclusion, str) or not conclusion.strip():
            raise ValueError("Conclusion must be a non-empty string")
        return conclusion.strip()

    def _next_id(self, prefix: str) -> str:
        self.counter += 1
        return f"{prefix}{self.counter:03d}"

    def add_rule(self, conditions: dict[str, Any], conclusion: str) -> str:
        conditions = self._validate_conditions(conditions)
        conclusion = self._validate_conclusion(conclusion)
        rule_id = self._next_id("R")
        self.rules[rule_id] = Rule(rule_id, conditions, conclusion)
        self.log("RULE_CREATED", {"rule_id": rule_id, "conditions": conditions,
                                   "conclusion": conclusion})
        return rule_id

    def add_example(self, attributes: dict[str, Any], conclusion: str) -> list[str]:
        attributes = self._validate_conditions(attributes)
        conclusion = self._validate_conclusion(conclusion)
        example = {"attributes": attributes, "conclusion": conclusion}
        conflicts = []
        for rule in self.rules.values():
            if rule.status == "active" and self.matches(rule, attributes):
                if rule.conclusion != conclusion:
                    conflicts.append(rule.id)
        self.examples.append(deepcopy(example))
        self.log("EXAMPLE_LEARNED", {"example": example, "conflicts": conflicts})
        return conflicts

    @staticmethod
    def matches(rule: Rule, attributes: dict[str, Any]) -> bool:
        return all(key in attributes and attributes[key] == value
                   for key, value in rule.conditions.items())

    def query(self, attributes: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(attributes, dict):
            raise ValueError("Attributes must be an object")
        matched = [rule for rule in self.rules.values()
                   if rule.status == "active" and self.matches(rule, attributes)]
        if not matched:
            return {"status": "ABSTENTION", "answer": None,
                    "reason": "Insufficient knowledge", "rules": []}
        conclusions = sorted({rule.conclusion for rule in matched})
        if len(conclusions) > 1:
            return {"status": "CONFLICT", "answer": None,
                    "rules": [rule.id for rule in matched],
                    "conclusions": conclusions}
        return {"status": "ANSWER", "answer": conclusions[0],
                "rules": [rule.id for rule in matched]}

    def _candidate_for(self, rule: Rule, relevant: list[dict[str, Any]],
                       attribute: str) -> dict[str, Any] | None:
        if attribute in rule.conditions or not all(
            attribute in example["attributes"] for example in relevant
        ):
            return None

        groups: dict[str, dict[str, Any]] = {}
        for example in relevant:
            value = example["attributes"][attribute]
            value_id = json.dumps({"type": type(value).__name__, "value": value},
                                  sort_keys=True, ensure_ascii=False, allow_nan=False)
            group = groups.setdefault(value_id, {"value": value, "labels": []})
            group["labels"].append(example["conclusion"])

        if len(groups) < 2 or any(len(set(group["labels"])) != 1
                                  for group in groups.values()):
            return None

        sizes = [len(group["labels"]) for group in groups.values()]
        total = sum(sizes)
        purity = sum(max(group["labels"].count(label)
                         for label in set(group["labels"]))
                     for group in groups.values()) / total
        # Normalized balance rewards splits that do not isolate almost all data
        # into one branch. This is a transparent heuristic, not a probability.
        balance = (len(sizes) * min(sizes) / total) if sizes else 0.0
        complexity_penalty = 1.0 / (1.0 + len(rule.conditions) + len(groups))
        score = 0.60 * purity + 0.25 * balance + 0.15 * complexity_penalty
        children = [
            {"conditions": {**rule.conditions, attribute: group["value"]},
             "conclusion": group["labels"][0], "support": len(group["labels"])}
            for group in groups.values()
        ]
        return {
            "attribute": attribute,
            "heuristic_score": round(score, 6),
            "score_components": {"observed_purity": round(purity, 6),
                                  "split_balance": round(balance, 6),
                                  "complexity_penalty": round(complexity_penalty, 6)},
            "support": total,
            "children": children,
            "explanation": (
                f"The observed examples are separated by '{attribute}'; each "
                "resulting group has one observed conclusion. This is a proposal "
                "based only on the stored examples, not proof of general validity."
            ),
        }

    def propose_reorganizations(self, rule_id: str) -> list[dict[str, Any]]:
        if rule_id not in self.rules:
            raise ValueError(f"Unknown rule: {rule_id}")
        rule = self.rules[rule_id]
        if rule.status != "active":
            return []
        relevant = [example for example in self.examples
                    if self.matches(rule, example["attributes"])]
        if len({example["conclusion"] for example in relevant}) < 2:
            return []

        keys = sorted({key for example in relevant
                       for key in example["attributes"]})
        candidates = [candidate for key in keys
                      if (candidate := self._candidate_for(rule, relevant, key))]
        candidates.sort(key=lambda candidate: (-candidate["heuristic_score"],
                                                candidate["attribute"]))
        proposals = []
        for candidate in candidates:
            proposal_id = self._next_id("P")
            proposal = {"id": proposal_id, "parent": rule_id,
                        "attribute": candidate["attribute"],
                        "heuristic_score": candidate["heuristic_score"],
                        "score_components": candidate["score_components"],
                        "support": candidate["support"],
                        "children": candidate["children"],
                        "explanation": candidate["explanation"],
                        "status": "PENDING"}
            self.proposals[proposal_id] = proposal
            proposals.append(deepcopy(proposal))
            self.log("REORGANIZATION_PROPOSED", proposal)
        return proposals

    def propose_reorganization(self, rule_id: str) -> dict[str, Any] | None:
        """Backward-compatible convenience method returning the top candidate."""
        proposals = self.propose_reorganizations(rule_id)
        return proposals[0] if proposals else None

    def validate(self, proposal_id: str, approved: bool) -> dict[str, Any]:
        if not isinstance(approved, bool):
            raise ValueError("Approval must be a boolean")
        if proposal_id not in self.proposals:
            raise ValueError(f"Unknown proposal: {proposal_id}")
        proposal = self.proposals[proposal_id]
        if proposal["status"] != "PENDING":
            raise ValueError("Proposal already processed")
        parent = self.rules.get(proposal["parent"])
        if parent is None or parent.status != "active":
            raise ValueError("Parent rule is no longer active")
        if approved:
            new_rules = []
            for child in proposal["children"]:
                conditions = self._validate_conditions(child["conditions"])
                conclusion = self._validate_conclusion(child["conclusion"])
                new_rules.append(Rule(self._next_id("R"), conditions,
                                      conclusion, parent=parent.id))
            # Apply only after all candidate rules have passed validation.
            parent.status = "archived"
            for child_rule in new_rules:
                self.rules[child_rule.id] = child_rule
            proposal["status"] = "APPROVED"
            proposal["created_rules"] = [rule.id for rule in new_rules]
        else:
            proposal["status"] = "REJECTED"
        self.log("HUMAN_VALIDATION", {"proposal": proposal_id,
                                      "approved": approved})
        return deepcopy(proposal)

    def state(self) -> dict[str, Any]:
        return {"schema_version": SCHEMA_VERSION,
                "rules": [asdict(rule) for rule in self.rules.values()],
                "examples": deepcopy(self.examples),
                "proposals": deepcopy(self.proposals),
                "history": deepcopy(self.history), "counter": self.counter}

    def save(self, filename: str | os.PathLike[str] = "anos_memory.json") -> None:
        """Write a complete snapshot atomically to avoid partial JSON files."""
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        content = json.dumps(self.state(), ensure_ascii=False, indent=2,
                             allow_nan=False)
        temporary_name = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8",
                                             dir=path.parent, delete=False) as file:
                temporary_name = file.name
                file.write(content)
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary_name, path)
        finally:
            if temporary_name and os.path.exists(temporary_name):
                os.unlink(temporary_name)

    @classmethod
    def load(cls, filename: str | os.PathLike[str]) -> "AnosOmniRSAK":
        """Load a snapshot created by ``save``; reject unknown schema versions."""
        with open(filename, encoding="utf-8") as file:
            state = json.load(file)
        if not isinstance(state, dict) or state.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("Unsupported or missing RSAK schema version")
        engine = cls()
        try:
            engine.rules = {item["id"]: Rule(**item) for item in state["rules"]}
            engine.examples = state["examples"]
            engine.proposals = state["proposals"]
            engine.history = state["history"]
            engine.counter = int(state["counter"])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Invalid RSAK snapshot structure") from error
        return engine


def demonstration() -> None:
    ai = AnosOmniRSAK()
    print("\n=== ANOS OMNI RSAK V2 — EXPERIMENTAL DEMO ===")
    rule = ai.add_rule({"wheels": 4}, "motorized")
    ai.add_example({"wheels": 4, "engine": True}, "motorized")
    conflicts = ai.add_example({"wheels": 4, "engine": False}, "not_motorized")
    print("Contradictions detected:", conflicts)
    proposal = ai.propose_reorganization(rule)
    print("Ranked, explainable proposal:\n",
          json.dumps(proposal, indent=2, ensure_ascii=False))
    if proposal:
        ai.validate(proposal["id"], True)
    print("Query:", ai.query({"wheels": 4, "engine": False}))


if __name__ == "__main__":
    demonstration()
