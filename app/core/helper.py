def maybe_unescape_text(text: str) -> str:
    # Decode only when text contains literal escape sequences
    try:
        return bytes(text, "utf-8").decode("unicode_escape")
    except Exception:
        return text