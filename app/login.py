from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.auth import create_access_token
from app.database import get_connection
from app.password import verify_password


router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(request: LoginRequest):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, password_hash FROM users WHERE username = %s",
                (request.username,),
            )
            user = cursor.fetchone()

    if user is None or not verify_password(request.password, user[1]):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    access_token = create_access_token(user[0])

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }