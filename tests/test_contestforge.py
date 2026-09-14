import json
from pathlib import Path
from contestforge_r.models import ProblemSpec
from contestforge_r.verification import run_solver, verify_problem
from contestforge_r.difficulty import estimate_difficulty
from contestforge_r.scoring import score_submission
from contestforge_r.pipeline import evaluate_pipeline

ROOT = Path(__file__).parents[1]


def test_spec_and_schema_round_trip():
    spec = ProblemSpec.from_json(ROOT / "examples/sum_pairs.json")
    assert spec.to_dict()["id"] == "sum-pairs"
    assert spec.json_schema()["$schema"].endswith("schema")


def test_verification_and_timeout():
    spec = ProblemSpec.from_json(ROOT / "examples/sum_pairs.json")
    result = verify_problem(spec, [{"numbers": [1, 4, 2, 3], "target": 5}])
    assert result.passed and result.cases == 1
    stuck = "import time; time.sleep(1)"
    assert not run_solver(stuck, {}, timeout=.01).ok


def test_population_and_reward():
    spec = ProblemSpec.from_json(ROOT / "examples/sum_pairs.json")
    estimate = estimate_difficulty({"good": spec.reference_solution}, [{"numbers": [1, 4], "target": 5}], spec.reference_solution)
    assert estimate.solved == 1
    reward = score_submission(verification_passed=True, difficulty_score=50)
    assert 0 <= reward.total <= 100
    pipeline = evaluate_pipeline(spec, [{"numbers": [1, 4], "target": 5}],
                                {"good": spec.reference_solution})
    assert pipeline.verification.passed
