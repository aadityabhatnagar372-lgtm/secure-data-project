from fastapi import FastAPI, HTTPException

from app.database import get_connection

app = FastAPI(title="Customer Data Node 2")


@app.get("/health")
def health_check():
    return {
        "node": "customer-node-2",
        "status": "healthy",
    }


@app.get("/customer/{customer_id}/email")
def get_customer_email(customer_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT email FROM customers WHERE id = %s",
                (customer_id,),
            )
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