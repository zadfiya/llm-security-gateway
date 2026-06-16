import re
from app.guardrails.input_guardrails import Detection
from app.guardrails.constants import OUTPUT_PATTERNS
from dataclasses import dataclass, field

# ─── Data classes ────────────────────────────────────────────────────────────

@dataclass
class OutputGuardResult:
    text: str
    detections: list = field(default_factory=list)