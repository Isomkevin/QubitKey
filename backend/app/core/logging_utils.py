"""Logging helpers that avoid leaking secrets."""

from __future__ import annotations

import logging
import re

_SENSITIVE = re.compile(
    r"(secret|otpauth|otp|token|password|private[_-]?key|authorization)",
    re.IGNORECASE,
)


class RedactingFilter(logging.Filter):
    """Best-effort redaction for accidental secret-like fields in log messages."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            msg = record.getMessage()
        except Exception:
            return True
        if _SENSITIVE.search(msg):
            record.msg = "[REDACTED sensitive log content]"
            record.args = ()
        return True


def configure_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    if not root.handlers:
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        )
    for handler in root.handlers:
        handler.addFilter(RedactingFilter())
