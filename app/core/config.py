from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):

    app_env: str = "development"

    # LLM provider selection: openai | groq | ollama
    llm_provider: str

    # API keys — loaded from env or Azure Key Vault in production
    openai_api_key: str 
    groq_api_key: str
    ollama_base_url: str

    # Rate limiting
    rate_limit_requests: int   # per minute per IP
    rate_limit_window: int

    use_keyvault: bool = False
    azure_keyvault_url: str = ""    # e.g. https://myvault.vault.azure.net/

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
