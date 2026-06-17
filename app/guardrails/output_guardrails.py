import re
from app.guardrails.input_guardrails import Detection
from app.guardrails.constants import OUTPUT_PATTERNS
from dataclasses import dataclass, field

# ─── Data classes ────────────────────────────────────────────────────────────

@dataclass
class OutputGuardResult:
    text: str
    detections: list = field(default_factory=list)

def scan_output(text: str) -> OutputGuardResult:
    """
    Scans LLM response for any PII or sensitive data.
    Always redacts — never blocks (response has already been generated).
    """
    detections: list[Detection] = []
    sanitized = text
    
    for label, pattern in OUTPUT_PATTERNS.items():
        if re.search(pattern):
            sanitized = re.sub(pattern, )
            detections.append(Detection(pattern_type=label, severity="high"))

    return OutputGuardResult(text=sanitized, detections=detections)