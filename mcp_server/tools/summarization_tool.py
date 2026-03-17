from typing import Generator
from constants import MODEL_NAME
from common.init_client import get_client
from common.style_print import GREEN, RESET

def summarize_text(text: str, compression_ratio: float = 0.3) -> Generator[str, None, None]:
    """Stream a summary of *text* compressed to roughly *compression_ratio* length.

    *compression_ratio* should be between 0.1 and 0.8.
    """
    client = get_client()
    if not text.strip():
        yield "Error: text cannot be blank."
        return
    ratio = max(0.1, min(compression_ratio, 0.8))
    system_prompt = (
        "You are a world‑class summarizer. Reduce the following text to about "
        f"{int(ratio*100)}% of its original length while preserving key ideas."
    )
    _stream = client.chat.completions.create(
        model = MODEL_NAME,
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        stream = True,
        # temperature = 0.5,
    )
    partial = ""
    for chunk in _stream:
        delta = getattr(chunk.choices[0].delta, "content", None)
        if delta:
            partial += delta
            yield partial

print(f"{GREEN} Loaded summarize_text tool. ✅ {RESET}")