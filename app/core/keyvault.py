from config import get_settings

def get_secret(secret_name: str) -> str:
    """
    Fetches a secret from Azure Key Vault.
    Returns cached value if within TTL to avoid per-request AKV latency (~20-50ms).
    Falls back to environment variable if USE_KEYVAULT=false.
    """

    settings = get_settings()

    if not settings.use_keyvault:
        # Local dev: resolve from env via config
        return _resolve_from_env(secret_name, settings)
    
    # Fetch from AKV
    try:
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient

    except Exception as e:
        pass
    

def _resolve_from_env(secret_name: str, settings) -> str:
    """Maps AKV secret names to config fields for local dev fallback."""
    mapping = {
        "groq-api-key" :   settings.groq_api_key,
        "openai-api-key" : settings.openai_api_key,
    }
    return mapping.get(secret_name, "")
