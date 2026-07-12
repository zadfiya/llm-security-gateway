from groq import Groq
from app.providers.base import BaseLLMProvider, CompletionResult, UsageDetails
from app.core.config import get_settings


class GroqProvider(BaseLLMProvider):
    def __init__(self):
        settings = get_settings()
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = "qwen/qwen3-32b"

    async def complete(self, prompt: str) -> CompletionResult:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            temperature=0.7
        )
        usage = UsageDetails()
        if getattr(response, "usage", None):
            usage.completion_tokens = getattr(response.usage, "completion_tokens", 0) or 0
            usage.prompt_tokens = getattr(response.usage, "prompt_tokens", 0) or 0
            usage.total_tokens = getattr(response.usage, "total_tokens", 0) or 0
            usage.completion_time = float(getattr(response.usage, "completion_time", 0.0) or 0.0)
            usage.queue_time = float(getattr(response.usage, "queue_time", 0.0) or 0.0)
            usage.total_time = float(getattr(response.usage, "total_time", 0.0) or 0.0)

        return CompletionResult(
            text=(response.choices[0].message.content or ""),
            usage=usage,
        )

    # async def complete(self, prompt: str) -> str:
    #     response = await self.client.generate(
    #         model="groq-2",
    #         input=prompt,
    #         max_tokens=2048,
    #         temperature=0.7,
    #     )
    #     return response.text

    def provider_name(self) -> str:
        return "Groq"