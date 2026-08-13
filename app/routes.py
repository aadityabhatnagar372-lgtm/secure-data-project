import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import APIRouter, Depends, Header, HTTPException

from app.access_key import AccessKeyRequest, generate_access_key
from app.access_key_store import get_access_key, store_access_key
from app.audit import audit_event
from app.auth import get_current_user
from app.data_minimizer import build_customer_select
from app.database import get_connection
from app.node_directory import get_primary_node, get_replica_nodes

router = APIRouter()


def check_customer_access(user_id: int, customer_id: int) -> bool:
    """Check whether the authenticated user owns the requested customer."""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT customer_id FROM users WHERE id = %s",
                (user_id,),
            )
            user = cursor.fetchone()

    if user is None:
        return False

    return user[0] == customer_id


def request_customer_email_from_node(customer_id: int) -> dict:
    """Request customer email from the primary, then replicas on failure."""
    primary = get_primary_node("customer")
    replicas = get_replica_nodes("customer")

    nodes = []

    if primary is not None:
        nodes.append(primary)

    nodes.extend(replicas)

    if not nodes:
        audit_event(
            "data_node_failover_exhausted",
            customer_id=customer_id,
            attempted_nodes=[],
        )

        raise HTTPException(
            status_code=503,
            detail="No customer data nodes are configured",
        )

    for node in nodes:
        url = f"http://{node.host}:{node.port}/customer/{customer_id}/email"

        request = Request(
            url,
            headers={"Accept": "application/json"},
            method="GET",
        )

        try:
            with urlopen(request, timeout=5) as response:
                return json.loads(response.read().decode("utf-8"))

        except HTTPError as exc:
            if exc.code == 404:
                raise HTTPException(
                    status_code=404,
                    detail="Customer not found",
                )

            audit_event(
                "data_node_error",
                node=node.name,
                customer_id=customer_id,
                error=f"http_{exc.code}",
            )

            continue

        except URLError:
            audit_event(
                "data_node_error",
                node=node.name,
                customer_id=customer_id,
                error="connection_error",
            )

            continue

    audit_event(
        "data_node_failover_exhausted",
        customer_id=customer_id,
        attempted_nodes=[node.name for node in nodes],
    )

    raise HTTPException(
        status_code=503,
        detail="All customer data nodes are unavailable",
    )


@router.get("/customer/{customer_id}/email")
def get_customer_email(
    customer_id: int,
    current_user_id: int = Depends(get_current_user),
    access_key: str | None = Header(default=None, alias="X-Access-Key"),
):
    if access_key is None:
        raise HTTPException(
            status_code=401,
            detail="Access key is required",
        )

    stored_key = get_access_key(access_key)

    if stored_key is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access key",
        )

    if stored_key["user_id"] != current_user_id:
        audit_event(
            "authorization_denied",
            user_id=current_user_id,
            customer_id=customer_id,
            reason="access_key_user_mismatch",
        )

        raise HTTPException(
            status_code=403,
            detail="Access key does not belong to the authenticated user",
        )

    if stored_key["customer_id"] != customer_id:
        audit_event(
            "authorization_denied",
            user_id=current_user_id,
            customer_id=customer_id,
            reason="access_key_customer_mismatch",
        )

        raise HTTPException(
            status_code=403,
            detail="Access key is not valid for this customer",
        )

    if stored_key["field"] != "email":
        audit_event(
            "authorization_denied",
            user_id=current_user_id,
            customer_id=customer_id,
            reason="access_key_field_mismatch",
        )

        raise HTTPException(
            status_code=403,
            detail="Access key is not valid for this field",
        )

    build_customer_select("email")

    result = request_customer_email_from_node(customer_id)

    audit_event(
        "customer_data_access",
        user_id=current_user_id,
        customer_id=customer_id,
        field="email",
    )

    return result


@router.post("/access-key")
def issue_access_key(
    request: AccessKeyRequest,
    current_user_id: int = Depends(get_current_user),
):
    if not check_customer_access(current_user_id, request.customer_id):
        audit_event(
            "authorization_denied",
            user_id=current_user_id,
            customer_id=request.customer_id,
            reason="customer_ownership_check_failed",
        )

        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this customer",
        )

    key = generate_access_key(
        user_id=current_user_id,
        customer_id=request.customer_id,
        field=request.field,
    )

    store_access_key(key)

    audit_event(
        "access_key_issued",
        user_id=current_user_id,
        customer_id=request.customer_id,
        field=request.field,
    )

    return {
        "access_key": key["token"],
        "customer_id": key["customer_id"],
        "field": key["field"],
        "expires_at": key["expires_at"],
    }