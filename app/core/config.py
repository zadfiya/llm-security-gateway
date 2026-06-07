from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings():

    app_env: str = "development"

    # LLM provider selection: openai | groq | ollama
    llm_provider: str = ""

    # Rate limiting
    rate_limit_requests: int = 60   # per minute per IP
    rate_limit_window: int = 60  

    use_keyvault: bool = False

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
