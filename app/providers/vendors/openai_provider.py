from openai import AsyncOpenAI
from app.providers.base import BaseLLMProvider, CompletionResult, UsageDetails
from app.core.config import get_settings


class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4o"

    async def complete(self, prompt: str) -> CompletionResult:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )

        usage = UsageDetails()
        if getattr(response, "usage", None):
            usage.completion_tokens = getattr(response.usage, "completion_tokens", 0) or 0
            usage.prompt_tokens = getattr(response.usage, "prompt_tokens", 0) or 0
            usage.total_tokens = getattr(response.usage, "total_tokens", 0) or 0

        # Best-effort extraction of text from various response shapes
        try:
            text = response.choices[0].message.content
            return CompletionResult(text=text or "", usage=usage)
        except Exception:
            # Fallbacks for different client implementations
            if hasattr(response, "text"):
                return CompletionResult(text=response.text or "", usage=usage)
            if isinstance(response, dict):
                choices = response.get("choices")
                if choices and isinstance(choices, list):
                    choice = choices[0]
                    if isinstance(choice, dict):
                        if "message" in choice and "content" in choice["message"]:
                            return CompletionResult(text=choice["message"]["content"] or "", usage=usage)
                        if "text" in choice:
                            return CompletionResult(text=choice["text"] or "", usage=usage)
            return CompletionResult(text=str(response), usage=usage)

    def provider_name(self) -> str:
        return "OpenAI"