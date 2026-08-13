from fastapi import FastAPI

app = FastAPI(title="Secure Distributed Data Access System")


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