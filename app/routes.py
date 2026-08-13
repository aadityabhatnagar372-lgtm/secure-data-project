from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.database import get_connection

router = APIRouter()


@router.get("/customer/{customer_id}/email")
def get_customer_email(
    customer_id: int,
    current_user_id: int = Depends(get_current_user),
):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT email FROM customers WHERE id = %s",
                (customer_id,),
            )
            customer = cursor.fetchone()

    if customer is None:
        return {
            "error": "Customer not found",
        }

    return {
        "customer_id": customer_id,
        "email": customer[0],
    }