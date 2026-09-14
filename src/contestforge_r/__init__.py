"""ContestForge-R: a small, reproducible contest-problem evaluation toolkit."""

from .models import Example, ProblemSpec
from .verification import VerificationResult, verify_problem
from .difficulty import DifficultyEstimate, estimate_difficulty
from .scoring import score_submission
from .pipeline import PipelineResult, evaluate_pipeline

__all__ = [
    "Example", "ProblemSpec", "VerificationResult", "verify_problem",
    "DifficultyEstimate", "estimate_difficulty", "score_submission",
    "PipelineResult", "evaluate_pipeline",
]
