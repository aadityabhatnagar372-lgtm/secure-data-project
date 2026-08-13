import logging
from typing import Any


logger = logging.getLogger("secure_data.audit")


def audit_event(event: str, **details: Any) -> None:
    """Record a structured security-relevant audit event."""
    safe_details = {
        key: value
        for key, value in details.items()
        if key not in {
            "password",
            "password_hash",
            "token",
            "access_key",
            "jwt",
            "secret",
            "encryption_key",
        }
    }

    logger.info(
        "audit_event=%s details=%s",
        event,
        safe_details,
    )