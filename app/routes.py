from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user
from app.data_minimizer import build_customer_select
from app.database import get_connection

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


@router.get("/customer/{customer_id}/email")
def get_customer_email(
    customer_id: int,
    current_user_id: int = Depends(get_current_user),
):
    if not check_customer_access(current_user_id, customer_id):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this customer",
        )

    query = build_customer_select("email")

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (customer_id,))
            customer = cursor.fetchone()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return {
        "customer_id": customer_id,
        "email": customer[0],
    }