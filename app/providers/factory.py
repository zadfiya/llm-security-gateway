from app.core.config import get_settings
from app.providers.base import BaseLLMProvider

def get_provider() -> BaseLLMProvider:
    """
    Returns the configured LLM provider instance.
    Add new providers here as elif branches.
    """
    settings = get_settings()
    provider = settings.llm_provider.lower()

    pass