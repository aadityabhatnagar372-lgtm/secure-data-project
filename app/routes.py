from fastapi import APIRouter

router = APIRouter()


@router.get("/customer/{customer_id}/email")
def get_customer_email(customer_id: int):
    return {
        "customer_id": customer_id,
        "email": "placeholder@example.com",
    }