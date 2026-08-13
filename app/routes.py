import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import APIRouter, Depends, Header, HTTPException

from app.access_key import AccessKeyRequest, generate_access_key
from app.access_key_store import get_access_key, store_access_key
from app.auth import get_current_user
from app.data_minimizer import build_customer_select
from app.database import get_connection
from app.node_directory import get_node_for_data

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
    """Request customer email data from the responsible data node."""
    node = get_node_for_data("customer")

    if node is None:
        raise HTTPException(
            status_code=503,
            detail="Customer data node is unavailable",
        )

    url = f"http://{node.host}:8001/customer/{customer_id}/email"

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

        raise HTTPException(
            status_code=502,
            detail="Customer data node returned an error",
        )

    except URLError:
        raise HTTPException(
            status_code=503,
            detail="Customer data node is unavailable",
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
        raise HTTPException(
            status_code=403,
            detail="Access key does not belong to the authenticated user",
        )

    if stored_key["customer_id"] != customer_id:
        raise HTTPException(
            status_code=403,
            detail="Access key is not valid for this customer",
        )

    if stored_key["field"] != "email":
        raise HTTPException(
            status_code=403,
            detail="Access key is not valid for this field",
        )

    build_customer_select("email")

    return request_customer_email_from_node(customer_id)


@router.post("/access-key")
def issue_access_key(
    request: AccessKeyRequest,
    current_user_id: int = Depends(get_current_user),
):
    if not check_customer_access(current_user_id, request.customer_id):
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

    return {
        "access_key": key["token"],
        "customer_id": key["customer_id"],
        "field": key["field"],
        "expires_at": key["expires_at"],
    }