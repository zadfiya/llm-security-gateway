import logging
import json
from pathlib import Path
from datetime import datetime, timezone

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)

# Dedicated logger for security gateway events
_logger = logging.getLogger("security_gateway")
_logger.setLevel(logging.INFO)

# File handler — one JSON object per line
_file_handler = logging.FileHandler("logs/security.log")
_file_handler.setFormatter(logging.Formatter("%(message)s"))
_logger.addHandler(_file_handler)

# Stdout handler for local dev visibility
_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(logging.Formatter("%(message)s"))
_logger.addHandler(_stream_handler)


def log_event( 
    original_input: str,
    sanitized_input: str,
    input_detections: list,
    blocked: bool,
    provider: str,
    response_snippet: str = "",
    output_detections: list = None,) -> None:
    """
    Writes one structured JSON log entry per request.
    Stores: timestamp, provider, block status, original query (capped),
    sanitized query, detections, and response snippet.
    """

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": provider,
        "blocked": blocked,
        "input": {
            "original": original_input[:500],
            "sanitized": sanitized_input[:500],
            "detections": [
                {
                    "type": d.pattern_type,
                    "severity": d.severity,
                    "redacted": d.redacted,
                }
                for d in input_detections
            ],
        },
        "output": {
            "snippet": response_snippet[:300],
            "detections": [
                {
                    "type": d.pattern_type,
                    "severity": d.severity,
                    "redacted": d.redacted,
                }
                for d in (output_detections or [])
            ],
        },
    }
    _logger.info(json.dumps(entry))
