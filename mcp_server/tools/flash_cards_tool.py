from typing import Generator
from constants import MODEL_NAME
from common.init_client import get_client
from common.style_print import GREEN, RESET

def generate_flashcards(topic: str, num_cards: int = 5) -> Generator[str, None, None]:
    """Stream *num_cards* Q/A flashcards for *topic* in JSON lines format."""
    client = get_client()
    if num_cards < 1 or num_cards > 20:
        yield "Error: num_cards must be between 1 and 20."
        return
    if not topic.strip():
        yield "Error: topic cannot be blank."
        return

    system_prompt = (
        "You are an AI that generates study flashcards. "
        'Return each flashcard on its own line as JSON: {"q": <question>, "a": <answer>}'
    )
    user_prompt = f"Create {num_cards} flashcards about {topic}."

    _stream = client.chat.completions.create(
        model = MODEL_NAME,
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        stream = True,
        # temperature = 0.8,
    )
    partial = ""
    for chunk in _stream:
        delta = getattr(chunk.choices[0].delta, "content", None)
        if delta:
            partial += delta
            yield partial

print(f"{GREEN} Loaded generate_flashcards tool. ✅ {RESET}")