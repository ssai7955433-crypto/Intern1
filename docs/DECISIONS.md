# Decision log

## 2026-10-11 — Ship a local deterministic baseline first

**Decision:** Use local BM25 retrieval with an extractive response as the default; make local Ollama generation optional.

**Reasoning:** The project should be reproducible without API credentials or an installed model. Returning retrieved policy text reduces paraphrase risk and makes it straightforward to inspect the evidence. Optional generation demonstrates prompt design while keeping the baseline testable offline.

**Trade-off:** BM25 may miss semantically similar wording that an embedding retriever could find. Evaluate a semantic/hybrid alternative if the corpus grows; retain an abstention path and compare on a held-out dataset.

## 2026-10-11 — Use synthetic policy content

**Decision:** Author fictional demo policies and label them as non-authoritative.

**Reasoning:** Real HR policy is sensitive, organization-specific, and can become harmful if treated as authoritative outside its source organization. Synthetic data makes the repository safe to share publicly and the workflow demonstrable.

**Trade-off:** The benchmark does not establish performance on any real company policy or legal requirements.

## 2026-10-11 — Cite section IDs and include excerpts

**Decision:** Cite source filename plus heading slug and return excerpt text with structured metadata.

**Reasoning:** A reviewer can inspect the policy file directly and compare the answer to its context. Stable heading-based IDs avoid line-number drift when documents are edited.

**Trade-off:** Duplicate headings in a document can create duplicate IDs; current sample documents use unique headings. A production ingestion pipeline should assign immutable document and passage IDs.

## 2026-10-11 — Fail closed on generation validation errors

**Decision:** Reject malformed, empty, or uncited local-model output and return an explicit backend error.

**Reasoning:** Falling back silently can hide provider failures and create success-shaped responses with unknown provenance.

**Trade-off:** An Ollama hiccup makes a request unavailable until corrected; users should retry or select the documented extractive baseline.
