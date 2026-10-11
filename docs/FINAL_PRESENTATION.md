# Final presentation — RAG Knowledge Assistant

Use the following as an 8-slide presentation outline. The project does not claim measured production impact; replace no metrics with estimates presented as facts.

## Slide 1 — Title

**RAG Knowledge Assistant**

Grounded answers from fictional company-policy documents
Project 1 · Generative AI Internship

## Slide 2 — User problem

- HR / People Operations service-desk analysts repeatedly search policy documents.
- A fluent answer without a source is hard to verify and unsafe to rely on.
- **Decision supported:** which policy section to consult and what it says.
- **Not supported:** eligibility decisions, legal advice, or automatic approvals.

## Slide 3 — Requirements and success

- Input: a plain-language policy question.
- Output: structured answer, support status, source / section citation, excerpt.
- Eleven answerable (including paraphrases) and three intentionally unanswerable benchmark cases.
- Baseline acceptance: 11/11 supported cases with expected source and terms; 3/3 abstentions; automated tests pass.
- These are project regression results, not measured user productivity or real-company accuracy.

## Slide 4 — Solution architecture

```text
Question -> input/safety validation -> BM25 over approved sections
         -> evidence threshold -> extractive answer + citation
         -> structured response
```

Optional extension: local Ollama generation, with JSON and citation-ID validation. Default mode runs offline with no API key.

## Slide 5 — Safety and trust

- Fictional data only; no question persistence or telemetry.
- Abstain when retrieval yields no evidence; refuse common prompt-override attempts.
- Treat source text as untrusted input to the model.
- Allow citations only from retrieved source sections.
- Citation membership is not entailment; humans verify policy interpretations.

## Slide 6 — Validation evidence

- Fixed evaluation dataset: 14 cases (11 supported, 3 unsupported).
- Automated tests cover retrieval, citations, abstention, invalid input, and prompt-override refusal.
- Run `python -m pytest` and `python -m evaluation.run_eval`.
- Report actual command output during the live demo; do not imply broader statistical validation.

## Slide 7 — Limitations and learning

- BM25 is lexical and can miss paraphrases.
- The synthetic corpus and tiny hand-authored set cannot represent real policies.
- No authentication, authorization, rate limiting, or production audit controls.
- Optional model citations can be valid IDs yet fail to support a claim.
- Biggest design choice: a deterministic extractive baseline prioritizes reproducibility and evidence inspection over fluent paraphrase.

## Slide 8 — Roadmap and close

1. Have policy owners approve/version the corpus.
2. Build a held-out, adversarial evaluation set with human-labeled citations.
3. Compare lexical and hybrid retrieval using the same cases.
4. Add identity-aware access control, operational monitoring, and privacy review.
5. Pilot with a human-in-the-loop workflow; measure search time and error rates before claiming benefit.

**Takeaway:** a useful policy assistant should show its evidence, validate its output, and say when the evidence is not enough.
