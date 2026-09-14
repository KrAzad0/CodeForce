"""Empirical difficulty estimates based on a solver population."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .verification import run_solver


@dataclass
class DifficultyEstimate:
    score: float
    solved: int
    total: int
    median_time_ms: float
    details: list[dict[str, Any]]


def estimate_difficulty(solvers: dict[str, str], inputs: list[Any],
                        reference: str, timeout: float = 2.0) -> DifficultyEstimate:
    details = []
    times = []
    solved = 0
    for name, source in solvers.items():
        passed = True
        elapsed = 0.0
        for case in inputs:
            result = run_solver(source, case, timeout)
            elapsed += result.elapsed_ms
            expected = run_solver(reference, case, timeout)
            if not result.ok or not expected.ok or result.output != expected.output:
                passed = False
                break
        if passed:
            solved += 1
        times.append(elapsed)
        details.append({"solver": name, "passed": passed, "elapsed_ms": elapsed})
    times.sort()
    median = times[len(times) // 2] if times else 0.0
    # 0 means everyone solves it; 100 means nobody does.
    score = round(100 * (1 - solved / len(solvers)), 2) if solvers else 0.0
    return DifficultyEstimate(score, solved, len(solvers), median, details)
