from fastapi import FastAPI

from app.routes import router

app = FastAPI(title="Secure Distributed Data Access System")

app.include_router(router)


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