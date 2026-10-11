from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from rag_assistant.engine import PolicyAssistant
from rag_assistant.schemas import AskRequest, AskResponse

app = FastAPI(
    title="RAG Knowledge Assistant",
    description="Answers questions from the fictional policy corpus with evidence citations.",
    version="1.0.0",
)
assistant = PolicyAssistant()

_DEMO_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f7f8fc">
  <title>Policy Assistant Demo</title>
  <style>
    :root { color-scheme: light; --ink:#172033; --muted:#697386; --line:#e4e8f0; --blue:#3157d5; --surface:#fff; }
    * { box-sizing:border-box; }
    body { margin:0; background:#f7f8fc; color:var(--ink); font:16px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; }
    main { width:min(820px,calc(100% - 32px)); margin:56px auto; }
    .eyebrow { color:var(--blue); font-size:.8rem; font-weight:750; letter-spacing:.12em; text-transform:uppercase; }
    h1 { margin:8px 0; font-size:clamp(2rem,5vw,3rem); line-height:1.1; letter-spacing:-.04em; }
    .intro { max-width:650px; color:var(--muted); }
    .notice { margin:24px 0; padding:12px 15px; border:1px solid #f1d995; border-radius:12px; background:#fff9e8; color:#614b13; font-size:.9rem; }
    .panel { padding:22px; border:1px solid var(--line); border-radius:18px; background:var(--surface); box-shadow:0 12px 36px #1720330b; }
    label { display:block; margin-bottom:8px; font-weight:700; }
    textarea { display:block; width:100%; min-height:108px; resize:vertical; padding:13px 14px; border:1px solid #cfd6e3; border-radius:11px; color:var(--ink); font:inherit; }
    textarea:focus { outline:3px solid #3157d52b; border-color:var(--blue); }
    button { margin-top:12px; padding:11px 17px; border:0; border-radius:10px; background:var(--blue); color:white; font:inherit; font-weight:700; cursor:pointer; }
    button:disabled { opacity:.6; cursor:wait; }
    .examples { display:flex; flex-wrap:wrap; gap:8px; margin:13px 0 0; }
    .example { padding:7px 10px; border:1px solid var(--line); border-radius:999px; background:white; color:#3b465c; font-size:.84rem; cursor:pointer; }
    #result { margin-top:20px; }
    .answer { padding:17px; border:1px solid var(--line); border-radius:13px; background:white; }
    .status { display:inline-block; margin-bottom:8px; padding:3px 9px; border-radius:999px; background:#e8efff; color:#2446b6; font-size:.76rem; font-weight:750; text-transform:uppercase; letter-spacing:.04em; }
    .status.insufficient_evidence,.status.refused { background:#fff2d8; color:#785400; }
    .citations { display:grid; gap:10px; margin-top:12px; }
    .citation { padding:13px 15px; border:1px solid var(--line); border-radius:12px; background:#fff; }
    .citation strong { display:block; margin-bottom:5px; font-size:.9rem; }
    .citation p { margin:0; color:#515c70; font-size:.9rem; }
    .error { color:#a32e2e; }
    footer { margin:25px 0; color:var(--muted); font-size:.83rem; }
    @media (max-width:520px) { main { margin:32px auto; } .panel { padding:16px; } }
  </style>
</head>
<body>
  <main>
    <div class="eyebrow">Knowledge assistant · live demo</div>
    <h1>Ask the policy handbook</h1>
    <p class="intro">Get a concise answer grounded in the demo policy documents. Every supported response includes its source so you can check the evidence.</p>
    <div class="notice"><strong>Demo content only:</strong> these fictional policies are not real HR, legal, or company guidance. Do not enter personal or confidential information.</div>
    <section class="panel" aria-label="Ask a policy question">
      <form id="ask-form">
        <label for="question">Your question</label>
        <textarea id="question" maxlength="1000" required placeholder="For example: How much notice is needed for planned remote work?"></textarea>
        <button id="submit" type="submit">Ask the assistant</button>
      </form>
      <div class="examples" aria-label="Example questions">
        <button class="example" type="button">How much paid parental leave is provided?</button>
        <button class="example" type="button">What approval is needed for a large purchase?</button>
        <button class="example" type="button">What is the daily travel per-diem rate?</button>
      </div>
    </section>
    <section id="result" aria-live="polite"></section>
    <footer>Answers may be incomplete or incorrect. Check the cited policy and contact its owner for authoritative guidance.</footer>
  </main>
  <script>
    const form = document.querySelector("#ask-form");
    const question = document.querySelector("#question");
    const submit = document.querySelector("#submit");
    const result = document.querySelector("#result");
    document.querySelectorAll(".example").forEach((button) => {
      button.addEventListener("click", () => { question.value = button.textContent; question.focus(); });
    });
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      submit.disabled = true;
      submit.textContent = "Searching policies…";
      result.replaceChildren();
      try {
        const response = await fetch("/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: question.value })
        });
        const payload = await response.json();
        if (!response.ok) throw new Error(payload.detail || "Request failed. Please try again.");
        const card = document.createElement("article");
        card.className = "answer";
        const status = document.createElement("span");
        status.className = `status ${payload.status}`;
        status.textContent = payload.status.replaceAll("_", " ");
        const answer = document.createElement("p");
        answer.textContent = payload.answer;
        card.append(status, answer);
        result.append(card);
        if (payload.citations.length) {
          const heading = document.createElement("h2");
          heading.textContent = "Sources";
          heading.style.fontSize = "1.05rem";
          result.append(heading);
          const citations = document.createElement("div");
          citations.className = "citations";
          payload.citations.forEach((item) => {
            const source = document.createElement("article");
            source.className = "citation";
            const title = document.createElement("strong");
            title.textContent = `${item.source} · ${item.section}`;
            const excerpt = document.createElement("p");
            excerpt.textContent = item.excerpt;
            source.append(title, excerpt);
            citations.append(source);
          });
          result.append(citations);
        }
      } catch (error) {
        const message = document.createElement("p");
        message.className = "error";
        message.textContent = error.message;
        result.append(message);
      } finally {
        submit.disabled = false;
        submit.textContent = "Ask the assistant";
      }
    });
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def demo() -> str:
    return _DEMO_PAGE


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
