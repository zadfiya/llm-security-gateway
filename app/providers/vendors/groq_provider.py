from groq import Groq
from app.providers.base import BaseLLMProvider
from app.core.config import get_settings


class GroqProvider(BaseLLMProvider):
    def __init__(self):
        settings = get_settings()
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = "qwen/qwen3-32b"

    async def complete(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            temperature=0.7
        )
        return response.choices[0].message.content

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