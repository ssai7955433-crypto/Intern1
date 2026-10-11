# Evaluation plan and baseline evidence

## Method

`evaluation/cases.json` contains eleven answerable questions tied to a policy file and expected text terms—including six paraphrased questions—and three questions that the sample corpus must not answer. `python -m evaluation.run_eval` runs each through the deterministic assistant and prints machine-readable JSON.

The evaluator checks:

- **Supported-answer accuracy:** a supported status, expected source present, expected terms present in the answer, and citations attached to the answer.
- **Abstention accuracy:** unsupported case receives `insufficient_evidence`.
- **Overall pass rate:** passing cases / total cases.
- **Citation integrity (unit tests):** every result points to a known indexed section; source and section are returned as structured fields.

## Acceptance threshold

The benchmark is a small regression gate. The declared baseline threshold is **14/14 cases (100%)**, with 11/11 supported and 3/3 abstentions. Failing any case exits the evaluator with a non-zero status.

To retain evidence for a review, run:

```powershell
python -m pytest
python -m evaluation.run_eval
```

The evaluator report is printed to the terminal. To save a report intentionally, redirect output to a dated evidence file outside tracked source or remove the generated report before committing; user and query data should not be added to public evidence.

## Test coverage and interpretation

Automated tests cover known-answer retrieval, citation validity, abstention, blank and overlong input, prompt override refusal, and all fixed benchmark cases. This does not test factual correctness on unseen policies, fairness, model-generated entailment, concurrency, API deployment security, or real-world user benefit.

The sample set is hand-authored and may overfit the implementation. Before a real pilot, have policy owners author a larger held-out set, include paraphrases and conflicting/outdated passages, label required citations, and report confidence intervals plus false-answer and false-abstention examples. Compare baseline and candidate retrieval/generation versions on exactly the same cases.
