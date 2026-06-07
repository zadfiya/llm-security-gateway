from fastapi import FastAPI
from app.routers import gateway
from app.middleware.rate_limit import RateLimitMiddleware

app = FastAPI(
    title="LLM Security Gateway",
    description="Security proxy layer for LLM API traffic",
    version="0.1.0",
)

# Middlewares
app.add_middleware(RateLimitMiddleware)

# Routers
app.include_router(gateway.router, prefix="/gateway", tags=["gateway"])


@app.get("/health")
async def health():
    return {"status": "Up and Running"}