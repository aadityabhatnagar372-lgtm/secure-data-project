import logging

from app.audit import audit_event


def test_audit_event_logs_safe_details(caplog):
    with caplog.at_level(logging.INFO, logger="secure_data.audit"):
        audit_event(
            "login_success",
            user_id=2,
            username="testuser",
        )

    assert "audit_event=login_success" in caplog.text
    assert "user_id" in caplog.text
    assert "testuser" in caplog.text


def test_audit_event_filters_sensitive_values(caplog):
    with caplog.at_level(logging.INFO, logger="secure_data.audit"):
        audit_event(
            "security_test",
            user_id=2,
            password="SECRET_PASSWORD",
            access_key="SECRET_ACCESS_KEY",
            jwt="SECRET_JWT",
            encryption_key="SECRET_ENCRYPTION_KEY",
            username="testuser",
        )

    assert "security_test" in caplog.text
    assert "testuser" in caplog.text

    assert "SECRET_PASSWORD" not in caplog.text
    assert "SECRET_ACCESS_KEY" not in caplog.text
    assert "SECRET_JWT" not in caplog.text
    assert "SECRET_ENCRYPTION_KEY" not in caplog.text