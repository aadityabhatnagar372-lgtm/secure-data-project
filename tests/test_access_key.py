from datetime import datetime, timedelta, timezone

import pytest

from app.access_key import generate_access_key
from app.access_key_store import get_access_key, store_access_key


def test_generate_access_key_contains_expected_scope():
    key = generate_access_key(
        user_id=2,
        customer_id=1,
        field="email",
    )

    assert key["token"]
    assert key["user_id"] == 2
    assert key["customer_id"] == 1
    assert key["field"] == "email"


def test_generate_access_key_expires_in_about_ten_minutes():
    before = datetime.now(timezone.utc)

    key = generate_access_key(
        user_id=2,
        customer_id=1,
        field="email",
    )

    after = datetime.now(timezone.utc)

    minimum_expiry = before + timedelta(minutes=10)
    maximum_expiry = after + timedelta(minutes=10)

    assert minimum_expiry <= key["expires_at"] <= maximum_expiry


def test_store_and_retrieve_access_key():
    key = generate_access_key(
        user_id=2,
        customer_id=1,
        field="email",
    )

    store_access_key(key)

    result = get_access_key(key["token"])

    assert result is not None
    assert result["user_id"] == 2
    assert result["customer_id"] == 1
    assert result["field"] == "email"


def test_expired_access_key_is_rejected():
    key = {
        "token": "expired-test-token",
        "user_id": 2,
        "customer_id": 1,
        "field": "email",
        "expires_at": datetime.now(timezone.utc) - timedelta(seconds=1),
    }

    store_access_key(key)

    assert get_access_key(key["token"]) is None
    assert get_access_key(key["token"]) is None