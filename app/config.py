import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env into environment variables (local dev)
load_dotenv()


@dataclass(frozen=True)
class Settings:
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    openai_embed_model: str = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

    # App
    app_env: str = os.getenv("APP_ENV", "dev")
    flask_host: str = os.getenv("FLASK_HOST", "0.0.0.0")
    #flask_port: int = int(os.getenv("FLASK_PORT", "8000"))
    flask_port: int = int(os.getenv("PORT", os.getenv("FLASK_PORT", "8000")))

    # RAG + memory
    rag_top_k: int = int(os.getenv("RAG_TOP_K", "5"))
    memory_max_turns: int = int(os.getenv("MEMORY_MAX_TURNS", "10"))

    def validate(self) -> None:
        if not self.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is missing. Add it to your .env file (do not commit .env)."
            )


settings = Settings()