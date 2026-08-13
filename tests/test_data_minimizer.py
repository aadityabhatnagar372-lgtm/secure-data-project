import pytest

from app.data_minimizer import (
    ALLOWED_CUSTOMER_FIELDS,
    build_customer_select,
    validate_customer_field,
)


def test_allowed_customer_fields():
    assert ALLOWED_CUSTOMER_FIELDS == {
        "email",
        "phone",
        "name",
    }


def test_validate_customer_field_accepts_email():
    assert validate_customer_field("email") == "email"


def test_validate_customer_field_rejects_unauthorized_field():
    with pytest.raises(ValueError, match="password_hash"):
        validate_customer_field("password_hash")


def test_build_customer_select_returns_only_requested_field():
    query = build_customer_select("email")

    assert query == (
        "SELECT email "
        "FROM customers "
        "WHERE id = %s"
    )


def test_build_customer_select_rejects_unauthorized_field():
    with pytest.raises(ValueError):
        build_customer_select("password_hash")