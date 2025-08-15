import streamlit as st
from services.llm_service import get_llm_response

st.title("LLM Chatbot")

if st.button("Clear Chat"):
    st.session_state.messages = []
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What can I help you with?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_llm_response(prompt)
            
            if response.startswith("Error:"):
                st.error(response)
            else:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})