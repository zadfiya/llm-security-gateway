from app.core.config import get_settings
from app.providers.base import BaseLLMProvider

def get_provider() -> BaseLLMProvider:
    """
    Returns the configured LLM provider instance.
    Add new providers here as elif branches.
    """
    settings = get_settings()
    provider = settings.llm_provider.lower()

    if provider == "openai":
        from app.providers.vendors.openai_provider import OpenAIProvider
        return OpenAIProvider()
    elif provider == "groq":
        from app.providers.vendors.groq_provider import GroqProvider
        return GroqProvider()
    elif provider == "ollama":
        from app.providers.vendors.ollama_provider import OllamaProvider
        return OllamaProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")