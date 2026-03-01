import json
from pathlib import Path

import faiss
import numpy as np

from app.llm.embeddings import embed_query


class FaissRetriever:
    def __init__(self, index_path: str = "indexes/faiss.index", meta_path: str = "indexes/metadata.jsonl"):
        self.index = faiss.read_index(index_path)
        self.meta = self._load_meta(meta_path)

    def _load_meta(self, meta_path: str) -> list[dict]:
        items = []
        with Path(meta_path).open("r", encoding="utf-8") as f:
            for line in f:
                items.append(json.loads(line))
        return items

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        q = embed_query(query)  # (1, dim)
        q = q.astype("float32")
        faiss.normalize_L2(q)

        scores, idxs = self.index.search(q, top_k)
        results = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx == -1:
                continue
            item = dict(self.meta[idx])
            item["score"] = float(score)
            results.append(item)
        return results