import re
from dataclasses import dataclass, field
from app.guardrails.constants import _SECURE_PROMPT, CRITICAL_PATTERNS

# ─── Data classes ────────────────────────────────────────────────────────────

@dataclass
class Detection:
    pattern_type: str   # e.g. "Credit Card", "SSN", "Email"
    severity: str       # "critical" | "high" | "low"
    redacted: bool      # True = sanitized, False = caused block


@dataclass
class GuardResult:
    text: str
    detections: list = field(default_factory=list)
    blocked: bool = False


def build_secure_prompt(user_input: str) -> str:
    """Wraps sanitized input in a LangChain security-aware prompt template."""
    return _SECURE_PROMPT.format(user_input=user_input)


# ─── Main scan function ───────────────────────────────────────────────────────

# TODO: Sanitize Prompt from injection or any Sensitive data and return resukt with detection stype

def scan_input(text: str) -> GuardResult:
    """
    1. Check for critical PII  → block immediately
    2. Redact high-severity PII
    3. Neutralize prompt injection
    4. Wrap in secure LangChain prompt
    """

    secure_text = build_secure_prompt(text)

    return GuardResult(text=secure_text, detections=None, blocked=False)

