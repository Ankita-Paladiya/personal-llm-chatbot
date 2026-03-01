from pathlib import Path
from app.llm.openai_client import chat_completion
from app.rag.retriever import FaissRetriever
from app.memory.store import MemoryStore
from app.config import settings


def load_prompt(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


class ChatEngine:
    def __init__(self):
        self.retriever = FaissRetriever()
        self.memory = MemoryStore()
        self.system_prompt = load_prompt("app/prompts/system.txt")
        self.rag_template = load_prompt("app/prompts/rag_template.txt")

    def build_context(self, query: str):
       results = self.retriever.search(query, top_k=settings.rag_top_k)
       return results

    def answer(self, user_id: str, question: str) -> dict:
       self.memory.add_message(user_id, "user", question)

       results = self.build_context(question)

       context_chunks = [r["text"] for r in results]
       context = "\n\n".join(context_chunks)

       user_prompt = self.rag_template.format(
           context=context,
           question=question
        )

       history = self.memory.get_recent_messages(user_id)

       messages = [{"role": "system", "content": self.system_prompt}]
       messages.extend(history)
       messages.append({"role": "user", "content": user_prompt})

       response = chat_completion(messages)

       self.memory.add_message(user_id, "assistant", response)

    # NEW: return sources
       sources = list({r["source"] for r in results})

       return {
        "answer": response,
        "sources": sources
       }