from fastapi import FastAPI

from app.login import router as login_router
from app.routes import router

app = FastAPI(title="Secure Distributed Data Access System")

app.include_router(router)
app.include_router(login_router)


@app.get("/")
def root():
    return {
        "message": "Secure Distributed Data Access System is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }