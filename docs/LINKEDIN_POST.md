# LinkedIn post draft

I built a **RAG Knowledge Assistant** to explore how an AI assistant can answer questions from policy documents while showing the source behind each answer.

The project includes a Python/FastAPI app, BM25 retrieval, cited answers, input and prompt-safety checks, and an explicit abstention when the demo handbook does not support an answer. It also has an optional local Ollama generation mode; the default demo works without an LLM service.

I tested it against **14 fixed evaluation cases**: 11 answerable questions (including paraphrases) and 3 questions that should be unanswerable from the sample handbook. The current implementation passed all 14 cases and all 22 automated tests. This is a small project regression set—not a guarantee of real-world accuracy or measured productivity improvement.

All included policy documents are fictional. This project is for demonstration and does not provide real HR or legal guidance.

Project repository: https://github.com/ssai7955433-crypto/Intern1

#GenerativeAI #RAG #Python #FastAPI #ResponsibleAI #SoftwareEngineering

## Suggested image order

1. `portfolio-assets/linkedin-project-cover.png` — project overview and workflow.
2. `portfolio-assets/linkedin-demo-preview.png` — illustrative interface preview with a cited answer.
3. `portfolio-assets/linkedin-evaluation.png` — fixed evaluation summary and limitation note.
