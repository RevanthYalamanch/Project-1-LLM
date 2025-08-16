import streamlit as st
import requests

st.title("LLM Model")

BACKEND_URL = "http://127.0.0.1:8000/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.feedback = {}
    st.rerun()

def send_feedback(message_id, feedback_type):
    st.session_state.feedback[message_id] = feedback_type
    st.toast("Thank you for your feedback!")

for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            message_id = f"msg_{idx}"
            if message_id not in st.session_state.feedback:
                col1, col2, _ = st.columns([1, 1, 10])
                with col1:
                    st.button("👍", key=f"thumbs_up_{idx}", on_click=send_feedback, args=(message_id, "positive"))
                with col2:
                    st.button("👎", key=f"thumbs_down_{idx}", on_click=send_feedback, args=(message_id, "negative"))

if prompt := st.chat_input("What can I help you with?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(BACKEND_URL, json={"message": prompt})
                response.raise_for_status()
                reply = response.json().get("reply")
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except requests.exceptions.RequestException as e:
                error_detail = e.response.json().get("detail") if e.response else str(e)
                st.error(f"Failed to get a response: {error_detail}")
