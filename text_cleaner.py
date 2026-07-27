import re


def clean_text(text: str) -> str:
    """Normalize resume text while keeping important technical symbols."""
    if not text:
        return ""

    text = text.lower()

    # Replace line breaks and tabs with spaces
    text = re.sub(r"[\n\r\t]+", " ", text)

    # Keep letters, numbers, +, #, dots and hyphens
    text = re.sub(r"[^a-z0-9+#.\-\s]", " ", text)

    # Remove repeated spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()