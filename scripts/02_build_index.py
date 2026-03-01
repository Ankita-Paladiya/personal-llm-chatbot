import json
from pathlib import Path

import faiss
import numpy as np

from app.llm.embeddings import embed_texts


def read_chunks(path: Path) -> list[dict]:
    chunks = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def main() -> None:
    chunks_path = Path("data/processed/chunks.jsonl")
    if not chunks_path.exists():
        raise RuntimeError("Run scripts/01_ingest_docs.py first. chunks.jsonl not found.")

    chunks = read_chunks(chunks_path)
    texts = [c["text"] for c in chunks]

    print(f"Embedding {len(texts)} chunks...")
    vectors = embed_texts(texts)  # (n, dim) float32

    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)  # inner product (works with cosine if normalized)

    # Normalize vectors so inner product ~= cosine similarity
    faiss.normalize_L2(vectors)

    index.add(vectors)

    out_dir = Path("indexes")
    out_dir.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(out_dir / "faiss.index"))

    # store metadata in same order as vectors
    with (out_dir / "metadata.jsonl").open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c) + "\n")

    print("✅ Saved FAISS index to indexes/faiss.index")
    print("✅ Saved metadata to indexes/metadata.jsonl")


if __name__ == "__main__":
    main()