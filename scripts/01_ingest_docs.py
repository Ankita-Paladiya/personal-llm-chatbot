import json
from pathlib import Path
from app.rag.chunking import load_and_chunk_folder


def main() -> None:
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)

    chunks = load_and_chunk_folder("data/raw")
    out_file = out_dir / "chunks.jsonl"

    with out_file.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps({"chunk_id": c.chunk_id, "text": c.text, "source": c.source}) + "\n")

    print(f"✅ Wrote {len(chunks)} chunks to {out_file}")


if __name__ == "__main__":
    main()