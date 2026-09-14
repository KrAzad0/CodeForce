"""One-call orchestration for verification, difficulty, and reward scoring."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .difficulty import DifficultyEstimate, estimate_difficulty
from .models import ProblemSpec
from .scoring import RewardScore, score_submission
from .verification import VerificationResult, verify_problem


@dataclass
class PipelineResult:
    verification: VerificationResult
    difficulty: DifficultyEstimate
    reward: RewardScore


def evaluate_pipeline(spec: ProblemSpec, inputs: list[Any],
                      solvers: dict[str, str] | None = None,
                      *, timeout: float = 2.0, quality: float = 1.0,
                      diversity: float = 1.0) -> PipelineResult:
    """Evaluate a spec with a shared corpus and return all audit-friendly signals."""
    verification = verify_problem(spec, inputs, timeout)
    population = solvers if solvers is not None else spec.metadata.get("solvers", {})
    difficulty = estimate_difficulty(population, inputs, spec.reference_solution, timeout)
    reward = score_submission(
        verification_passed=verification.passed,
        difficulty_score=difficulty.score,
        quality_score=quality,
        diversity_score=diversity,
    )
    return PipelineResult(verification, difficulty, reward)
