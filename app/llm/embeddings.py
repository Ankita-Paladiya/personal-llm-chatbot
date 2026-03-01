import numpy as np
from openai import OpenAI
from app.config import settings
from app.llm.openai_client import get_client


def embed_texts(texts: list[str]) -> np.ndarray:
    """
    Returns a numpy array of shape (n_texts, embed_dim) in float32 for FAISS.
    """
    client: OpenAI = get_client()
    resp = client.embeddings.create(
        model=settings.openai_embed_model,
        input=texts,
    )
    vectors = [item.embedding for item in resp.data]
    return np.array(vectors, dtype="float32")


def embed_query(text: str) -> np.ndarray:
    """
    Convenience: returns shape (1, embed_dim)
    """
    return embed_texts([text])