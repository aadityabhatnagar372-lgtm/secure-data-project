from typing import Final


ALLOWED_CUSTOMER_FIELDS: Final[set[str]] = {
    "email",
    "phone",
    "name",
}


def validate_customer_field(field: str) -> str:
    """Validate that a requested customer field is allowed."""
    if field not in ALLOWED_CUSTOMER_FIELDS:
        raise ValueError(f"Field '{field}' is not available for access.")

    return field


def build_customer_select(field: str) -> str:
    """Build a SELECT statement for one allowed customer field."""
    validated_field = validate_customer_field(field)

    return (
        f"SELECT {validated_field} "
        "FROM customers "
        "WHERE id = %s"
    )