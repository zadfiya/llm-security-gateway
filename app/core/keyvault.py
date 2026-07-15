def get_secret(secret_name: str) -> str:
    """
    Fetches a secret from Azure Key Vault.
    Returns cached value if within TTL to avoid per-request AKV latency (~20-50ms).
    Falls back to environment variable if USE_KEYVAULT=false.
    """

def _resolve_from_env(secret_name: str, settings) -> str:
    """Maps AKV secret names to config fields for local dev fallback."""