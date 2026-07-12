import httpx
from app.providers.base import BaseLLMProvider, CompletionResult, UsageDetails
from app.core.config import get_settings


class OllamaProvider(BaseLLMProvider):
    def __init__(self):
        settings = get_settings()
        self.base_url = settings.ollama_base_url
        self.model = "llama3"

    async def complete(self, prompt: str) -> CompletionResult:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
            )
            response.raise_for_status()
            data = response.json()

            prompt_tokens = int(data.get("prompt_eval_count") or 0)
            completion_tokens = int(data.get("eval_count") or 0)
            total_tokens = prompt_tokens + completion_tokens

            usage = UsageDetails(
                completion_tokens=completion_tokens,
                prompt_tokens=prompt_tokens,
                total_tokens=total_tokens,
                completion_time=float(data.get("eval_duration") or 0) / 1_000_000_000,
                queue_time=float(data.get("load_duration") or 0) / 1_000_000_000,
                total_time=float(data.get("total_duration") or 0) / 1_000_000_000,
            )

            return CompletionResult(text=(data.get("response") or ""), usage=usage)

    # async def complete(self, prompt: str) -> str:
    #     url = f"{self.base_url}/v1/chat/completions"
    #     payload = {
    #         "model": "llama3-8b-8192",
    #         "messages": [{"role": "user", "content": prompt}],
    #         "max_tokens": 2048,
    #         "temperature": 0.7
    #     }
    #     async with httpx.AsyncClient() as client:
    #         response = await client.post(url, json=payload)
    #         response.raise_for_status()
    #         data = response.json()
    #         return data["choices"][0]["message"]["content"]

    def provider_name(self) -> str:
        return "Ollama"