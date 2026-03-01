from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.chat_engine import ChatEngine

app = FastAPI(title="Personal LLM Chatbot API", version="1.0.0")
engine = ChatEngine()


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    user_id: str
    response: str
    sources: list[str] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.user_id.strip() or not req.message.strip():
        raise HTTPException(status_code=400, detail="user_id and message are required")

    result = engine.answer(req.user_id, req.message)

    # If your ChatEngine returns dict with sources (recommended)
    if isinstance(result, dict):
        answer = result.get("answer", "")
        sources = result.get("sources", [])
    else:
        # fallback if your engine still returns only string
        answer = str(result)
        sources = []

    return ChatResponse(user_id=req.user_id, response=answer, sources=sources)