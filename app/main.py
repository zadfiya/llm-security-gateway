from fastapi import FastAPI
from app.routers import gateway

app = FastAPI(
    title="LLM Security Gateway",
    description="Security proxy layer for LLM API traffic",
    version="0.1.0",
)

# TODO: Middleware

# Routers
app.include_router(gateway.router, prefix="/gateway", tags=["gateway"])


@app.get("/health")
async def health():
    return {"status": "Up and Running"}