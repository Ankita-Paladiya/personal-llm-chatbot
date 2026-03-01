import os
import requests
import streamlit as st

# --------------------
# Settings
# --------------------
API_URL = os.getenv("CHAT_API_URL", "http://127.0.0.1:8000/chat")

st.set_page_config(page_title="Personal Chatbot", page_icon="💬", layout="centered")
st.title("💬 Personal LLM Chatbot")
st.caption("RAG + Memory + Sources")

# --------------------
# Session state
# --------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = "user1"

if "messages" not in st.session_state:
    # each item: {"role": "user"|"assistant", "content": "...", "sources": [...] optional}
    st.session_state.messages = []

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    st.session_state.user_id = st.text_input("User ID", st.session_state.user_id)

    st.write("---")
    st.write("Backend")
    st.code(API_URL, language="text")

    if st.button("🧹 New chat (clear UI)"):
        st.session_state.messages = []
        st.rerun()

# --------------------
# Render chat history
# --------------------
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("sources"):
            with st.expander("Sources"):
                for s in m["sources"]:
                    st.write(f"- {s}")

# --------------------
# Chat input
# --------------------
prompt = st.chat_input("Type your message...")
if prompt:
    # show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # call backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(
                    API_URL,
                    json={"user_id": st.session_state.user_id, "message": prompt},
                    timeout=60,
                )
                if resp.status_code != 200:
                    st.error(f"API error {resp.status_code}: {resp.text}")
                else:
                    data = resp.json()
                    answer = data.get("response", "")
                    sources = data.get("sources", [])

                    st.markdown(answer)
                    if sources:
                        with st.expander("Sources"):
                            for s in sources:
                                st.write(f"- {s}")

                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer, "sources": sources}
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Could not reach backend API: {e}")