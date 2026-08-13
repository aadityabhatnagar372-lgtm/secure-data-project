from datetime import datetime, timezone


_ACCESS_KEYS: dict[str, dict] = {}


def store_access_key(access_key: dict) -> None:
    """Store an access key record in memory."""
    _ACCESS_KEYS[access_key["token"]] = access_key


def get_access_key(token: str) -> dict | None:
    """Return an access key record if it exists and is not expired."""
    access_key = _ACCESS_KEYS.get(token)

    if access_key is None:
        return None

    if access_key["expires_at"] <= datetime.now(timezone.utc):
        _ACCESS_KEYS.pop(token, None)
        return None

    return access_key