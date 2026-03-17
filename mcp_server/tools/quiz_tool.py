from typing import Generator
from constants import EXPLANATION_LEVELS, MODEL_NAME
from common.init_client import get_client
from common.style_print import GREEN, RESET

def quiz_me(topic: str, level: int = 3, num_questions: int = 5) -> Generator[str, None, None]:
    """Stream a quiz with numbered Qs then reveal answers after all questions."""
    client = get_client()
    if num_questions < 1 or num_questions > 15:
        yield "Error: num_questions must be between 1 and 15."
        return
    if not topic.strip():
        yield "Error: topic cannot be blank."
        return

    level_desc = EXPLANATION_LEVELS.get(level, "at an intermediate level")
    system_prompt = (
        "You are an AI quiz master. Generate a quiz of multiple‑choice questions "
        f"about {topic} {level_desc}. Number the questions. After listing all Qs, "
        "add an \nANSWER KEY section with the correct options."
    )

    _stream = client.chat.completions.create(
        model = MODEL_NAME,
        messages = [{"role": "system", "content": system_prompt}],
        stream = True,
        # temperature = 0.7,
    )
    partial = ""
    for chunk in _stream:
        delta = getattr(chunk.choices[0].delta, "content", None)
        if delta:
            partial += delta
            yield partial

print(f"{GREEN} Loaded quiz_me tool. ✅ {RESET}")