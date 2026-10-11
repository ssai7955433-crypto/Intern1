from __future__ import annotations

from fastapi import FastAPI, HTTPException

from rag_assistant.engine import PolicyAssistant
from rag_assistant.schemas import AskRequest, AskResponse

app = FastAPI(
    title="RAG Knowledge Assistant",
    description="Answers questions from the fictional policy corpus with evidence citations.",
    version="1.0.0",
)
assistant = PolicyAssistant()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/documents")
def documents() -> dict[str, list[str]]:
    return {"documents": sorted({chunk.source for chunk in assistant.chunks})}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    try:
        return assistant.answer(request.question)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
