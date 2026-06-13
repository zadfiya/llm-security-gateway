from openai import AsyncOpenAI
from app.providers.base import BaseLLMProvider
from app.core.config import get_settings

class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

     async def complete(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )
        return response.choices[0].message.content


    # async def complete(self, prompt: str) -> str:
    #     response = await self.client.chat.completions.create(
    #         model="gpt-4o",
    #         messages=[{"role": "user", "content": prompt}],
    #         max_tokens=2048,
    #         temperature=0.7
    #     )
    #     return response.choices[0].message.content

    def provider_name(self) -> str:
        return "OpenAI"