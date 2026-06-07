from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.providers.factory import get_provider

router = APIRouter()

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    provider: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main gateway endpoint.
    Guardrails + LLM call will be wired in next Sprint 2.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    provider = get_provider()

    # TODO Sprint 2: input_guard.scan(request.message)
    response_text = await provider.complete(request.message)
    # TODO Sprint 2: output_guard.scan(response_text)

    return ChatResponse(response=response_text, provider=provider.provider_name())

