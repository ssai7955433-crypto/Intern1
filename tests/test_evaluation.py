import json
from pathlib import Path

from evaluation.run_eval import evaluate
from rag_assistant.engine import PolicyAssistant

ROOT = Path(__file__).resolve().parents[1]


def test_curated_evaluation_set_meets_declared_baseline() -> None:
    cases = json.loads((ROOT / "evaluation" / "cases.json").read_text(encoding="utf-8"))
    report = evaluate(PolicyAssistant(policy_dir=ROOT / "data" / "policies"), cases)

    assert report["case_count"] == 8
    assert report["pass_rate"] == 1
    assert report["supported_answer_accuracy"] == 1
    assert report["abstention_accuracy"] == 1
