from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class UsageDetails:
    completion_tokens: int = 0
    prompt_tokens: int = 0
    total_tokens: int = 0
    completion_time: float = 0.0
    queue_time: float = 0.0
    total_time: float = 0.0


@dataclass
class CompletionResult:
    text: str
    usage: Optional[UsageDetails] = None


class BaseLLMProvider(ABC):
    """
    Abstract interface for LLM providers.
    Any new model = implement this class. No gateway changes needed.
    """

    @abstractmethod
    async def complete(self, prompt: str) -> CompletionResult:
        """Send prompt to the model, return text + usage details."""
        pass

    @abstractmethod
    def provider_name(self) -> str:
        """Return provider identifier for logging."""
        pass
