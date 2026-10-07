import os
from pathlib import Path
from dotenv import load_dotenv
import httpx

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2")


async def generate_response(messages: list, system: str) -> str:

    ollama_messages = [
        {
            "role": "system",
            "content": system
        }
    ]

    ollama_messages.extend(messages)

    payload = {
        "model": MODEL_NAME,
        "messages": ollama_messages,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=120.0) as client:

        response = await client.post(
            OLLAMA_URL,
            json=payload
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]