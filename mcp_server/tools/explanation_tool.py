
from typing import Generator
from constants import EXPLANATION_LEVELS, MODEL_NAME
from common.init_client import get_client
from common.style_print import GREEN, RESET

def explain_concept(question: str, level: int) -> Generator[str, None, None]:
    """Stream an explanation of *question* at the requested *level* (1‑5). If 1, explanation would be like we are talking to a 5 year old and if 5, explanation would be technical and complex."""
    client = get_client()
    if not question.strip():
        yield "Error: question cannot be blank."
        return

    level_desc = EXPLANATION_LEVELS.get(level, "clearly and concisely")
    system_prompt = "You are a helpful AI Tutor. Explain the following concept " f"{level_desc}."
    _stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        stream=True,
        # temperature=0.7,
    )
    partial = ""
    for chunk in _stream:
        delta = getattr(chunk.choices[0].delta, "content", None)
        if delta:
            partial += delta
            yield partial

print(f"{GREEN} Loaded explain_concept tool. ✅ {RESET}")