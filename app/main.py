from flask import Flask, request, jsonify
from app.chat_engine import ChatEngine
from app.config import settings

app = Flask(__name__)
engine = ChatEngine()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    if not data or "user_id" not in data or "message" not in data:
        return jsonify({"error": "Missing user_id or message"}), 400

    user_id = data["user_id"]
    message = data["message"]

    result = engine.answer(user_id, message)

    return jsonify({
       "user_id": user_id,
       "response": result["answer"],
       "sources": result["sources"]
    })
if __name__ == "__main__":
    app.run(host=settings.flask_host, port=settings.flask_port, debug=True)