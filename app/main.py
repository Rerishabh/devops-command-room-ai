import os
from fastapi import FastAPI, HTTPException

app = FastAPI(title="DevOps Command Room Target Service")


@app.get("/")
def read_root():
    return {"status": "online", "system": "DevOps Command Room"}


@app.get("/health")
def health_check():
    service_status = os.getenv("SERVICE_STATUS", "healthy")
    if service_status == "healthy":
        return {"status": "healthy", "uptime_s": 3600}
    if service_status == "degraded":
        raise HTTPException(
            status_code=500,
            detail="Service degraded: memory leak detected"
        )
    raise HTTPException(
        status_code=500,
        detail=f"Service degraded: {service_status}"
    )
