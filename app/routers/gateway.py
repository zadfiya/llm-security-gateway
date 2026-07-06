from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.providers.factory import get_provider
from app.guardrails.input_guardrails import scan_input
from app.guardrails.output_guardrails import scan_output
from app.core.logger import log_event

router = APIRouter()

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    provider: str
    warnings: list[str] = []


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main gateway endpoint.
    Guardrails + LLM call will be wired in next Sprint 2.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    provider = get_provider()

    input_result = scan_input(request.message)

    if input_result.blocked:
        log_event(
            original_input=request.message,
            sanitized_input="[BLOCKED]",
            input_detections=input_result.detections,
            blocked=True,
            provider="none",
        )
        raise HTTPException(
            status_code=400,
            detail=(
                "Request blocked: critical sensitive data detected "
                f"({input_result.detections[0].pattern_type}). "
                "Remove sensitive information and retry."
            ),
        )

    print (f"Guard Result: text={input_result.text} blocked={input_result.blocked}, detections={input_result.detections}")
    response_text = await provider.complete(input_result.text)

    output_result = scan_output(response_text)

    warnings = []
    if input_result.detections:
        warnings.append(f"Input: {len(input_result.detections)} field(s) redacted before sending to LLM")
    if output_result.detections:
        warnings.append(f"Output: {len(output_result.detections)} field(s) redacted from LLM response")

    return ChatResponse(
        response=output_result.text,
        provider=provider.provider_name(),
        warnings=warnings,
    )

