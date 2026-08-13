from fastapi import FastAPI

app = FastAPI(title="Customer Data Node 3")


@app.get("/health")
def health_check():
    return {
        "node": "customer-node-3",
        "status": "healthy",
    }