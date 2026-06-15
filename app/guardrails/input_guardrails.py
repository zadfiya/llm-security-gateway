from dataclasses import dataclass, field

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