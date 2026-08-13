from fastapi import FastAPI

app = FastAPI(title="Customer Data Node")


@app.get("/health")
def health_check():
    return {
        "node": "customer-node-1",
        "status": "healthy",
    }