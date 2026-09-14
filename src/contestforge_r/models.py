"""JSON-backed domain models. The package intentionally uses only the standard library."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any


@dataclass
class Example:
    input: Any
    output: Any
    explanation: str = ""


@dataclass
class ProblemSpec:
    id: str
    title: str
    statement: str
    input_format: str
    output_format: str
    constraints: list[str] = field(default_factory=list)
    examples: list[Example] = field(default_factory=list)
    generator: str | None = None
    reference_solution: str | None = None
    brute_force_solution: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id or not self.title or not self.statement:
            raise ValueError("id, title, and statement are required")
        if not self.reference_solution:
            raise ValueError("reference_solution is required")

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        return value

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True) + "\n"

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "ProblemSpec":
        data = dict(value)
        data["examples"] = [Example(**e) if isinstance(e, dict) else e for e in data.get("examples", [])]
        return cls(**data)

    @classmethod
    def from_json(cls, path: str | Path) -> "ProblemSpec":
        return cls.from_dict(json.loads(Path(path).read_text()))

    def write_json(self, path: str | Path) -> None:
        Path(path).write_text(self.to_json())

    @staticmethod
    def json_schema() -> dict[str, Any]:
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "ContestForge ProblemSpec",
            "type": "object",
            "required": ["id", "title", "statement", "input_format", "output_format", "reference_solution"],
            "properties": {
                "id": {"type": "string", "minLength": 1},
                "title": {"type": "string", "minLength": 1},
                "statement": {"type": "string", "minLength": 1},
                "input_format": {"type": "string"},
                "output_format": {"type": "string"},
                "constraints": {"type": "array", "items": {"type": "string"}},
                "examples": {"type": "array", "items": {"$ref": "#/$defs/example"}},
                "generator": {"type": ["string", "null"]},
                "reference_solution": {"type": "string"},
                "brute_force_solution": {"type": ["string", "null"]},
                "metadata": {"type": "object"},
            },
            "$defs": {"example": {
                "type": "object", "required": ["input", "output"],
                "properties": {"input": {}, "output": {}, "explanation": {"type": "string"}},
            }},
        }
