from fastapi import FastAPI


app = FastAPI(title="API for monitoring", version="1.0")


@app.get("/health")
async def health_status() -> dict:
    """returns status"""
    return {"status": "healthy"}


@app.get("message/{id}")
async def get_message_id(id: int) -> dict:
    """returns message from a simulated database"""
    return {"id": id}


@app.post("/process")
async def process_data(data: str) -> dict:
    """processes data"""
    pass


@app.get("/metrics")
async def get_metrics() -> dict:
    """metrics with Prometheus"""
    pass

