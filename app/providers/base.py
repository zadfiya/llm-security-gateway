from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """
    Abstract interface for LLM providers.
    Any new model = implement this class. No gateway changes needed.
    """

    @abstractmethod
    async def complete(self, prompt: str) -> str:
        """Send prompt to the model, return response text."""
        pass

    @abstractmethod
    def provider_name(self) -> str:
        """Return provider identifier for logging."""
        pass
