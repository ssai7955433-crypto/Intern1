# Problem framing and requirements

**Status:** Baseline project scope
**Scenario:** An employee-support analyst needs to locate an answer in a small set of approved policy documents without losing the source passage.

## Stakeholder and decision

- **Primary user:** HR / People Operations service-desk analyst.
- **Secondary users:** Employees seeking a policy reference; mentor/reviewer evaluating answer quality.
- **Decision enabled:** Which policy section to consult and what its stated provision says. The assistant does not decide eligibility, approve a request, interpret law, or replace an authorized policy owner.
- **Expected benefit:** Reduce repeated manual searching for routine policy references while making source verification a first-class part of every supported answer. The project measures retrieval, abstention, and citation behavior; it does not claim measured time savings or production impact.

## Inputs, outputs, and boundaries

| Item | Definition |
|---|---|
| Inputs | One plain-text question (1–1,000 characters); curated Markdown sample policies |
| Output | JSON with `status`, `answer`, and citations (`source`, `section`, stable citation ID, excerpt) |
| In scope | Local retrieval, cited evidence response, conservative abstention, input validation, offline regression evaluation |
| Out of scope | Real company policies, employment decisions, legal advice, confidential-data ingestion, identity/access management, write actions, document upload |
| Operating constraint | Baseline runs locally without an LLM, API key, network, or vector database |

## Success measures and acceptance criteria

The fixed fourteen-case benchmark has eleven supported questions (including six paraphrases) and three unanswerable questions. A passing baseline run must:

1. Find the expected source and exact expected answer terms in all eleven supported cases.
2. Include only citations corresponding to indexed policy sections.
3. Abstain on all three questions not answerable from the sample policy corpus.
4. Reject empty and overlong questions; refuse common attempts to override instructions or expose the system prompt.
5. Respond to a standalone greeting with a short welcome and supported-topic suggestions; do not treat a greeting prefix as a replacement for a policy question.
6. Pass the automated tests from a clean install.

The target on this small deterministic set is 100% for each measure. This is a regression gate, not a statistical guarantee. The test set is intentionally small; see [evaluation notes](EVALUATION.md).

## Quality attributes

- **Grounding:** Every answer cites retrieved passages; default answers quote evidence instead of generating unsupported paraphrases.
- **Traceability:** Citations identify the source file and heading; response includes excerpt text.
- **Privacy:** No telemetry or persistence; default processing is local.
- **Reliability:** Invalid input and backend failures produce explicit errors; there are no success-shaped fallbacks.
- **Reviewability:** Policies, evaluation cases, code, test results, and design decisions are included in version control.

## Requirement-to-evidence map

| Requirement | Implementation / evidence |
|---|---|
| Approved context | `data/policies/*.md` |
| Prompt and output design | `rag_assistant/engine.py`, `rag_assistant/schemas.py` |
| Retrieval and citations | `PolicyAssistant.retrieve`, `PolicyAssistant.answer` |
| Structured API | `rag_assistant/api.py` |
| Safety controls | `rag_assistant/safety.py`, `docs/SAFETY_AND_PRIVACY.md` |
| Evaluation | `evaluation/cases.json`, `evaluation/run_eval.py`, `tests/test_evaluation.py` |
| Reproduction and demo | `README.md`, `docs/DEMO_SCRIPT.md` |
