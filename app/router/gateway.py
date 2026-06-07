from pydantic import BaseModel
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

    provider = "Open AI"

    # TODO Sprint 2: input_guard.scan(request.message)
    response_text = "LLM response"
    # TODO Sprint 2: output_guard.scan(response_text)

    return ChatResponse(response=response_text, provider=provider)

