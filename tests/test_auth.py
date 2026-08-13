import time

import jwt
import pytest
from fastapi.security import HTTPAuthorizationCredentials

from app.auth import create_access_token, get_current_user


def test_create_access_token_contains_user_and_expiration():
    token = create_access_token(2)

    payload = jwt.decode(
        token,
        options={"verify_signature": False},
    )

    assert payload["sub"] == "2"
    assert "exp" in payload
    assert payload["exp"] > int(time.time())


def test_get_current_user_returns_user_id_from_valid_token():
    token = create_access_token(2)

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    result = get_current_user(credentials)

    assert result == 2


def test_get_current_user_rejects_invalid_token():
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="invalid-token",
    )

    with pytest.raises(Exception):
        get_current_user(credentials)