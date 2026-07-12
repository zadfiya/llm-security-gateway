from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.providers.factory import get_provider
from app.guardrails.input_guardrails import scan_input
from app.guardrails.output_guardrails import scan_output
from app.core.logger import log_event
from app.core.helper import maybe_unescape_text
from app.providers.base import UsageDetails

router = APIRouter()

class ChatRequest(BaseModel):
    message: str


class UsageResponse(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    completion_time: float
    queue_time: float
    total_time: float


class ChatResponse(BaseModel):
    response: str
    provider: str
    warnings: list[str] = []
    usage: list[UsageResponse] = []


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

    completion_result = await provider.complete(input_result.text)
    response_text = maybe_unescape_text(completion_result.text)

    output_result = scan_output(response_text)

    warnings = []
    if input_result.detections:
        warnings.append(f"Input: {len(input_result.detections)} field(s) redacted before sending to LLM")
    if output_result.detections:
        warnings.append(f"Output: {len(output_result.detections)} field(s) redacted from LLM response")

    log_event(
        original_input=request.message,
        sanitized_input=input_result.text,
        input_detections=input_result.detections,
        blocked=False,
        provider=provider.provider_name(),
        response_snippet=output_result.text,
        output_detections=output_result.detections,
    )

    usage_entries: list[UsageResponse] = []
    if completion_result.usage:
        usage: UsageDetails = completion_result.usage
        usage_entries.append(
            UsageResponse(
                completion_tokens=usage.completion_tokens,
                prompt_tokens=usage.prompt_tokens,
                total_tokens=usage.total_tokens,
                completion_time=usage.completion_time,
                queue_time=usage.queue_time,
                total_time=usage.total_time,
            )
        )

    return ChatResponse(
        response=output_result.text,
        provider=provider.provider_name(),
        warnings=warnings,
        usage=usage_entries,
    )

