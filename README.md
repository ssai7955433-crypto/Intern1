# RAG Knowledge Assistant

A small, reproducible retrieval-augmented assistant for a **fictional** company-policy handbook. It retrieves policy passages, returns source citations, abstains when evidence is weak, and can optionally use a local Ollama model to draft a grounded answer.

> **Demo data only.** The policies in `data/policies/` are invented for this project. They are not legal, HR, security, or operational advice and must not be substituted for approved company policy.

## Project at a glance

| | |
|---|---|
| Primary user | HR / People Operations service-desk analyst |
| Decision enabled | Where to find an applicable policy provision and what it says |
| Input | A question about the included policy documents |
| Output | A structured answer, support status, and citations to retrieved policy sections |
| Baseline | Local BM25 retrieval plus extractive, cited evidence; no model or network required |
| Optional generation | Ollama running locally, enabled with `RAG_LLM_MODE=ollama` |

The baseline intentionally prefers a short quotation over an unsupported paraphrase. This is a demonstration and evaluation package, not a production HR decision-maker.

## Acceptance criteria and evidence

| Acceptance criterion | Evidence |
|---|---|
| Scope, stakeholder, constraints, success measures documented | [Requirements](docs/REQUIREMENTS.md) |
| Repeatable architecture and decisions recorded | [Architecture](docs/ARCHITECTURE.md), [decision log](docs/DECISIONS.md) |
| Grounded answers with traceable policy citations | `rag_assistant/engine.py`, API response `citations` |
| Structured output and invalid-input handling | Pydantic request/response models in `rag_assistant/api.py`; tests in `tests/` |
| Safety and privacy controls / limitations | [Safety and privacy](docs/SAFETY_AND_PRIVACY.md) |
| Fixed evaluation cases and reproducible score output | [Evaluation cases](evaluation/cases.json), [evaluation guide](docs/EVALUATION.md), `evaluation/run_eval.py` |
| Mentor can run, test, and demo from a clean checkout | Commands below; [demo script](docs/DEMO_SCRIPT.md) |
| Presentation-ready project summary | [Final presentation](docs/FINAL_PRESENTATION.md) |

## Portfolio and LinkedIn assets

PNG visuals and a ready-to-edit, evidence-based post draft are in [portfolio-assets/](portfolio-assets/) and [LinkedIn post draft](docs/LINKEDIN_POST.md). The UI image is labeled as an illustrative preview, and the evaluation visual explicitly describes the limits of the small fixed test set.

## Quick start

Requires Python 3.10 or newer.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn rag_assistant.api:app --reload
```

Open <http://127.0.0.1:8000/> for the chat-style demo or <http://127.0.0.1:8000/docs> for interactive API documentation. The policy corpus is loaded from the repository; no upload or external service is required.

## Deploy free on Render

This repository includes a Render Blueprint at `render.yaml`, configured for a free Python web service. To publish a public URL:

1. Push this repository to GitHub, then click:

   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ssai7955433-crypto/Intern1)

   Or sign in to [Render](https://render.com/) and choose **New → Blueprint**.
2. Connect the GitHub account that can access `ssai7955433-crypto/Intern1`, select this repository and its `main` branch, then apply the `render.yaml` configuration.
3. Wait for the build to finish. Render will show the public service URL; open that URL for the browser demo or append `/docs` for API docs.

The free service may spin down after inactivity and take some time to respond on its first request. It uses the deterministic extractive baseline and needs no API key or paid LLM. A deployment cannot be created on your behalf without authorization to a hosting account.

Ask a question:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/ask `
  -ContentType "application/json" `
  -Body '{"question":"How much notice is required for planned remote work?"}'
```

Example response shape:

```json
{
  "status": "supported",
  "answer": "For a planned remote-work arrangement, submit the request to your manager at least five business days before it starts. [remote-work.md#Requesting-a-remote-work-arrangement]",
  "citations": [
    {
      "source": "remote-work.md",
      "section": "Requesting a remote-work arrangement",
      "citation": "remote-work.md#Requesting-a-remote-work-arrangement",
      "excerpt": "..."
    }
  ]
}
```

Standalone greetings such as `Hi` receive a brief welcome and examples of supported policy topics. If no passage clears the retrieval threshold, the API returns `status: "insufficient_evidence"` and no citations. It does not ask the model to fill gaps.

## Run checks and evaluation

```powershell
python -m pytest
python -m evaluation.run_eval
```

The evaluator prints a JSON report with case count, supported-answer accuracy, abstention accuracy, citation validity, and per-case results. The thresholds and known limitations are defined in [Evaluation](docs/EVALUATION.md). Evaluation is a small deterministic regression set, not a claim of real-world HR accuracy.

## Optional local LLM generation

The default extractive mode requires no model. To enable local Ollama generation:

1. Install and start Ollama: <https://ollama.com/download>.
2. Pull a model, for example `ollama pull qwen3:4b`.
3. Set the environment variables and start the API:

```powershell
$env:RAG_LLM_MODE = "ollama"
$env:OLLAMA_MODEL = "qwen3:4b"
python -m uvicorn rag_assistant.api:app --reload
```

The model receives only the question and retrieved excerpts. Its JSON output is schema-checked; citations not present in the retrieved context are rejected. This verifies citation membership, **not** semantic entailment. Ollama errors are surfaced as API errors rather than silently converted into a successful answer.

## Repository map

```text
Intern1/
├── README.md
├── app.py
├── requirements.txt
├── rag_assistant/
│   ├── api.py
│   ├── engine.py
│   ├── safety.py
│   └── schemas.py
├── data/policies/                 # Fictional, curated demo handbook
├── evaluation/
│   ├── cases.json
│   └── run_eval.py
├── tests/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DECISIONS.md
│   ├── DEMO_SCRIPT.md
│   ├── EVALUATION.md
│   ├── FINAL_PRESENTATION.md
│   ├── REQUIREMENTS.md
│   └── SAFETY_AND_PRIVACY.md
└── .gitignore
```

## Scope and next steps

The package uses a tiny static Markdown corpus and a transparent local BM25 index. It does not ingest confidential files, authenticate callers, persist questions, or make employment decisions. See [Safety and privacy](docs/SAFETY_AND_PRIVACY.md) for the full limitations and a production-readiness roadmap.
