"""Command line interface for ContestForge-R."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from .models import ProblemSpec
from .verification import verify_problem
from .difficulty import estimate_difficulty


def _spec(path: str) -> ProblemSpec:
    return ProblemSpec.from_json(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="contestforge")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate"); validate.add_argument("spec")
    verify = sub.add_parser("verify"); verify.add_argument("spec"); verify.add_argument("inputs")
    estimate = sub.add_parser("estimate"); estimate.add_argument("spec"); estimate.add_argument("inputs")
    args = parser.parse_args(argv)
    spec = _spec(args.spec)
    if args.command == "validate":
        print(json.dumps(spec.json_schema(), indent=2)); return 0
    inputs = json.loads(Path(args.inputs).read_text())
    if args.command == "verify":
        result = verify_problem(spec, inputs)
        print(json.dumps(result.__dict__, indent=2))
        return 0 if result.passed else 1
    if args.command == "estimate":
        solvers = spec.metadata.get("solvers", {})
        result = estimate_difficulty(solvers, inputs, spec.reference_solution)
        print(json.dumps(result.__dict__, indent=2)); return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
