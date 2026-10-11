# Safety, privacy, and limitations

## Controls in this demo

- Uses only fictional, version-controlled policy documents.
- Processes questions in memory; does not persist prompts, answers, or telemetry.
- Rejects blank and overlong questions and refuses a small set of recognizable prompt-override / system-prompt-exfiltration attempts.
- Treats retrieved text as untrusted instructions in the optional generation prompt.
- Provides an explicit insufficient-evidence status and no citations when retrieval has no above-threshold match.
- Constrains local-model citations to IDs in the retrieved passages and surfaces malformed model responses as errors.
- Uses a local-only Ollama endpoint by default (`127.0.0.1`); no external LLM is called.

## Limitations and residual risks

1. The guard patterns are not a complete prompt-injection defense. The best control is to avoid sending sensitive data and keep retrieved content bounded and trusted.
2. BM25 matching and a score threshold cannot establish semantic relevance or correctness. A lexically matching but irrelevant passage may still be retrieved.
3. Citation allow-list validation checks that an ID exists in retrieved context, not that the cited passage supports every claim. LLM output requires human review.
4. The corpus and test set are synthetic, tiny, and authored by the project developer. Results do not generalize to a real organization.
5. There is no authentication, authorization, rate limiting, audit log, encryption-at-rest layer, or tenant isolation. Do not expose this demo API to the public internet.
6. The policy text is not legal or HR advice. The assistant must not make hiring, performance, leave-eligibility, disciplinary, or other consequential decisions.
7. `GET /documents` and citations expose file names and excerpts; deploy only with an approved public corpus.
8. Optional Ollama mode's behavior depends on the locally installed model and its version; offline evaluation covers the deterministic extractive baseline, not generated prose.

## Privacy and responsible-use rules

- Do not add real employee records, case details, health information, credentials, or confidential policy files to this public demo.
- For an organizational pilot, use approved data, approved hosting, least-privilege access, retention controls, and a privacy/security review before connecting any user data.
- Direct users to the policy owner or People Operations when the policy is ambiguous, conflicting, outdated, or incomplete.

## Production-readiness roadmap

1. Obtain policy-owner approval, classify content, maintain document version/effective-date metadata, and implement a review/publishing workflow.
2. Add identity-aware access control, authorization-filtered retrieval, rate limiting, input/output size limits, secrets management, and security monitoring.
3. Build representative and adversarial evaluations with policy-owner labels; measure retrieval recall, answer support, citation precision, abstention quality, and subgroup impacts.
4. Add semantic/hybrid retrieval only after a baseline comparison; preserve source metadata and document-level access filters.
5. Add audit and retention controls that meet company requirements, with redaction and explicit privacy notices.
6. Require human review for policy interpretation or consequential action; provide a correction and escalation route.
