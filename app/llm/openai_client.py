from openai import OpenAI
from app.config import settings


def get_client() -> OpenAI:
    settings.validate()
    return OpenAI(api_key=settings.openai_api_key)


def chat_completion(messages: list[dict], temperature: float = 0.2) -> str:
    """
    messages format:
    [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."}
    ]
    """
    client = get_client()
    resp = client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content or ""