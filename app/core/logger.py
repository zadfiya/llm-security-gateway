import logging
from pathlib import Path

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


def log_event() -> None:
    """
    Writes one structured JSON log entry per request.
    Stores: timestamp, provider, block status, original query (capped),
    sanitized query, detections, and response snippet.
    """
    # Implementation of the logging logic goes here
    pass