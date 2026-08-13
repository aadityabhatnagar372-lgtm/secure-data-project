import secrets
from datetime import datetime, timedelta, timezone


ACCESS_KEY_EXPIRE_MINUTES = 10


def generate_access_key(
    user_id: int,
    customer_id: int,
    field: str,
) -> dict:
    """Generate a scoped access key valid for 10 minutes."""
    token = secrets.token_urlsafe(32)

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_KEY_EXPIRE_MINUTES
    )

    return {
        "token": token,
        "user_id": user_id,
        "customer_id": customer_id,
        "field": field,
        "expires_at": expires_at,
    }