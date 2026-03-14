import os
import requests
import streamlit as st

API_URL = os.getenv("CHAT_API_URL", "http://127.0.0.1:8000/chat")

st.set_page_config(page_title="Personal Chatbot", page_icon="💬")
st.title("💬 Personal LLM Chatbot")
st.caption("RAG + Memory + Sources")

if "user_id" not in st.session_state:
    st.session_state.user_id = "user1"

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Settings")
    st.session_state.user_id = st.text_input("User ID", st.session_state.user_id)

    if st.button("🧹 New chat (clear UI)"):
        st.session_state.messages = []
        st.rerun()

# render history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("sources"):
            with st.expander("Sources"):
                for s in m["sources"]:
                    st.write(f"- {s}")

prompt = st.chat_input("Type your message...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                r = requests.post(
                    API_URL,
                    json={"user_id": st.session_state.user_id, "message": prompt},
                    timeout=120,
                )

                if r.status_code != 200:
                    st.error(f"API error {r.status_code}: {r.text}")
                else:
                    data = r.json()
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
                st.error(f"Could not reach backend: {e}")