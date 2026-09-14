"""Reward scoring for a generated-problem pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class RewardScore:
    total: float
    correctness: float
    difficulty: float
    quality: float
    diversity: float


def score_submission(*, verification_passed: bool, difficulty_score: float,
                     quality_score: float = 1.0, diversity_score: float = 1.0,
                     weights: dict[str, float] | None = None) -> RewardScore:
    """Combine normalized pipeline signals into a score in [0, 100]."""
    weights = weights or {"correctness": .5, "difficulty": .25, "quality": .15, "diversity": .10}
    correctness = 1.0 if verification_passed else 0.0
    difficulty = max(0.0, min(1.0, difficulty_score / 100))
    quality = max(0.0, min(1.0, quality_score))
    diversity = max(0.0, min(1.0, diversity_score))
    total = 100 * (weights["correctness"] * correctness + weights["difficulty"] * difficulty +
                   weights["quality"] * quality + weights["diversity"] * diversity)
    return RewardScore(round(total, 2), correctness, difficulty, quality, diversity)
