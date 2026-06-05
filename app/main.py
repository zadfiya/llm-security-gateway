from fastapi import FastAPI

app = FastAPI(
    title="LLM Security Gateway",
    description="Security proxy layer for LLM API traffic",
    version="0.1.0",
)

# TODO: Middleware

# TODO :Routers


@app.get("/health")
async def health():
    return {"status": "ok"}