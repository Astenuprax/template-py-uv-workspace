"""Best-effort observability setup.

No-op safe: if ``logfire`` is not installed/configured, this returns cleanly
without emitting telemetry or requiring credentials, so the template runs
anywhere. Wire a real exporter by installing ``logfire`` and setting its token.
"""

import importlib
from typing import Any


def configure_tracing(*, service_name: str = "platform-core") -> None:
    """Configure tracing if ``logfire`` is available; otherwise do nothing."""
    try:
        logfire: Any = importlib.import_module("logfire")
    except ImportError:
        return
    logfire.configure(service_name=service_name, send_to_logfire=False)
    instrument = getattr(logfire, "instrument_pydantic_ai", None)
    if callable(instrument):
        instrument()
