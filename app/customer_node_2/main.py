from fastapi import FastAPI

app = FastAPI(title="Customer Data Node 2")


@app.get("/health")
def health_check():
    return {
        "node": "customer-node-2",
        "status": "healthy",
    }