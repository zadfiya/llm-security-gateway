from dataclasses import dataclass, field

# ─── Data classes ────────────────────────────────────────────────────────────

@dataclass
class OutputGuardResult:
    text: str
    detections: list = field(default_factory=list)