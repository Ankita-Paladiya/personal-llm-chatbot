from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Chunk:
    chunk_id: str
    text: str
    source: str


def simple_chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    """
    Simple character-based chunker (easy to understand).
    Later we can upgrade to token-based chunking.
    """
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        start = max(end - overlap, end)  # overlap
    return chunks


def load_and_chunk_folder(raw_dir: str = "data/raw") -> list[Chunk]:
    raw_path = Path(raw_dir)
    files = sorted(list(raw_path.glob("*.txt")))

    all_chunks: list[Chunk] = []
    for f in files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        pieces = simple_chunk_text(content)

        for i, piece in enumerate(pieces):
            chunk_id = f"{f.stem}_{i}"
            all_chunks.append(Chunk(chunk_id=chunk_id, text=piece, source=str(f)))

    return all_chunks