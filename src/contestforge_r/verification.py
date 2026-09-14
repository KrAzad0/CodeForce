"""Run contestant/reference programs safely enough for local verification."""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from .models import ProblemSpec


@dataclass
class RunResult:
    ok: bool
    output: Any = None
    stdout: str = ""
    stderr: str = ""
    elapsed_ms: float = 0
    error: str | None = None


@dataclass
class VerificationResult:
    passed: bool
    cases: int
    failures: list[dict[str, Any]] = field(default_factory=list)


def _source_arg(source: str) -> tuple[list[str], str | None]:
    try:
        path = Path(source)
        if path.exists() and path.is_file():
            return [sys.executable, str(path)], None
    except OSError:
        # A source string can be longer than a legal filesystem path.
        pass
    return [sys.executable, "-c", source], None


def run_solver(source: str, input_data: Any, timeout: float = 2.0) -> RunResult:
    """Execute a solver with one JSON value on stdin and JSON on stdout.

    A solver may print whitespace around its JSON result. A timeout or malformed
    result is reported as data rather than escaping as an exception.
    """
    import time
    command, _ = _source_arg(source)
    payload = json.dumps(input_data)
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            command, input=payload, text=True, capture_output=True,
            timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return RunResult(False, stdout=exc.stdout or "", stderr=exc.stderr or "",
                         elapsed_ms=(time.perf_counter() - start) * 1000,
                         error=f"timeout after {timeout:.3f}s")
    except OSError as exc:
        return RunResult(False, elapsed_ms=(time.perf_counter() - start) * 1000,
                         error=f"could not start solver: {exc}")
    elapsed = (time.perf_counter() - start) * 1000
    if proc.returncode:
        return RunResult(False, stdout=proc.stdout, stderr=proc.stderr,
                         elapsed_ms=elapsed, error=f"exit code {proc.returncode}")
    try:
        output = json.loads(proc.stdout.strip())
    except json.JSONDecodeError as exc:
        return RunResult(False, stdout=proc.stdout, stderr=proc.stderr,
                         elapsed_ms=elapsed, error=f"invalid JSON output: {exc.msg}")
    return RunResult(True, output, proc.stdout, proc.stderr, elapsed)


def verify_problem(spec: ProblemSpec, inputs: list[Any], timeout: float = 2.0) -> VerificationResult:
    """Compare reference and brute-force outputs for every supplied input."""
    if not spec.brute_force_solution:
        raise ValueError("brute_force_solution is required for verification")
    failures = []
    for index, case in enumerate(inputs):
        reference = run_solver(spec.reference_solution, case, timeout)
        brute = run_solver(spec.brute_force_solution, case, timeout)
        if not reference.ok or not brute.ok or reference.output != brute.output:
            failures.append({
                "index": index, "input": case,
                "reference": reference.output if reference.ok else reference.error,
                "brute_force": brute.output if brute.ok else brute.error,
            })
    return VerificationResult(not failures, len(inputs), failures)
