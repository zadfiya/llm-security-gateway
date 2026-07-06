from openai import AsyncOpenAI
from app.providers.base import BaseLLMProvider
from app.core.config import get_settings


class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4o"

    async def complete(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )

        # Best-effort extraction of text from various response shapes
        try:
            return response.choices[0].message.content
        except Exception:
            # Fallbacks for different client implementations
            if hasattr(response, "text"):
                return response.text
            if isinstance(response, dict):
                choices = response.get("choices")
                if choices and isinstance(choices, list):
                    choice = choices[0]
                    if isinstance(choice, dict):
                        if "message" in choice and "content" in choice["message"]:
                            return choice["message"]["content"]
                        if "text" in choice:
                            return choice["text"]
            return str(response)

    def provider_name(self) -> str:
        return "OpenAI"