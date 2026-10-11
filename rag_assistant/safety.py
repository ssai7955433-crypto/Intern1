from __future__ import annotations

import re

MAX_QUESTION_LENGTH = 1000
_OVERRIDE_PATTERNS = (
    re.compile(r"\bignore\s+(all\s+)?(previous|prior|above)\s+instructions?\b", re.I),
    re.compile(r"\b(reveal|show|print|repeat)\s+(the\s+)?(system|developer)\s+prompt\b", re.I),
    re.compile(r"\bpretend\s+you\s+have\s+no\s+rules\b", re.I),
)
_GREETING_PATTERN = re.compile(
    r"^(?:hi|hello|hey|hiya|good morning|good afternoon|good evening)[!. ,]*$",
    re.I,
)


def validate_question(question: str) -> str | None:
    """Return a safe-to-process question, or a user-facing refusal reason."""
    normalized = question.strip()
    if not normalized:
        raise ValueError("Question must not be empty.")
    if len(normalized) > MAX_QUESTION_LENGTH:
        raise ValueError(f"Question must be at most {MAX_QUESTION_LENGTH} characters.")
    if any(pattern.search(normalized) for pattern in _OVERRIDE_PATTERNS):
        return "I can only help answer questions using the approved policy documents."
    return None


def is_greeting(question: str) -> bool:
    """Identify standalone greetings without intercepting policy questions."""
    return _GREETING_PATTERN.fullmatch(question.strip()) is not None
