import streamlit as st
import requests
import uuid

st.title("ex-codhar")


if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input():
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.spinner("Working..."):
        try:
            response = requests.post(
                url="http://localhost:8008/request_agent",
                json={
                    "session_id": str(st.session_state.session_id),
                    "user_query": prompt
                }
            )
            parsed_response = response.json()

            with st.chat_message("assistant"):
                st.markdown(parsed_response["ai_response"])
            st.session_state.messages.append({
                "role": "assistant",
                "content": parsed_response["ai_response"]
            })
        except Exception as e:
            st.error(str(e))