from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from rag_assistant.engine import PolicyAssistant

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evaluation" / "cases.json"


def evaluate(assistant: PolicyAssistant, cases: list[dict[str, Any]]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for case in cases:
        response = assistant.answer(case["question"])
        citations = {citation.source for citation in response.citations}
        if case["should_abstain"]:
            passed = response.status == "insufficient_evidence"
        else:
            passed = (
                response.status == "supported"
                and case["expected_source"] in citations
                and all(term.lower() in response.answer.lower() for term in case["expected_terms"])
                and all(
                    citation.citation in response.answer
                    for citation in response.citations[:2]
                )
            )
        results.append(
            {
                "id": case["id"],
                "passed": passed,
                "status": response.status,
                "expected_source_found": (
                    case["expected_source"] is not None
                    and case["expected_source"] in citations
                ),
                "citation_count": len(response.citations),
            }
        )

    supported = [case for case in cases if not case["should_abstain"]]
    abstentions = [case for case in cases if case["should_abstain"]]
    report = {
        "case_count": len(cases),
        "pass_count": sum(result["passed"] for result in results),
        "pass_rate": sum(result["passed"] for result in results) / len(results) if results else 0,
        "supported_answer_accuracy": (
            sum(result["passed"] for result in results if result["id"] in {c["id"] for c in supported})
            / len(supported)
            if supported
            else 0
        ),
        "abstention_accuracy": (
            sum(result["passed"] for result in results if result["id"] in {c["id"] for c in abstentions})
            / len(abstentions)
            if abstentions
            else 0
        ),
        "results": results,
    }
    return report


def main() -> None:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    report = evaluate(PolicyAssistant(), cases)
    print(json.dumps(report, indent=2))
    if report["pass_rate"] < 1:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
