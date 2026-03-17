import os
from dotenv import load_dotenv
from openai import OpenAI
from common.style_print import GREEN, RED, RESET

print(f"{GREEN}Loading environment variables... {RESET}")
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError(f"{RED} OPENAI_API_KEY not found in environment variables. ❌ {RESET}")
else:
    print(f"{GREEN} All API keys loaded successfully. ✅ {RESET}")

def get_client() -> OpenAI:
    """Return an initialized OpenAI client."""
    client = OpenAI(api_key = openai_api_key)
    return client   