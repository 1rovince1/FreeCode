import streamlit as st
import requests
import uuid

st.title("ex-codhar")
SERVER_URL = "http://localhost:8008"

with st.sidebar:
    response = requests.get(
        url=SERVER_URL + "/all_active_sessions"
    )
    active_sessions = response.json()["active_sessions"]
    NEW_SESSION = "NEW_SESSION"

    sessions = [NEW_SESSION] + active_sessions

    selected_session = st.selectbox(
        label="sessions",
        options=sessions,
        format_func=lambda x:(
            "new_session" if x == NEW_SESSION 
            else str(x[0])
        )
    )

if selected_session == NEW_SESSION:
    st.session_state.session_id = uuid.uuid4()
    st.session_state.messages = []
else:
    st.session_state.session_id = selected_session[0]
    st.session_state.messages = selected_session[1]["session_messages"]


# if "messages" not in st.session_state:
#     st.session_state.messages = selected_session["session_messages"]
# if "session_id" not in st.session_state:
#     st.session_state.session_id = uuid.uuid4()

# st.session_state.messages = selected_session[1]["session_messages"]
# st.session_state.session_id = selected_session[0]

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
                url=SERVER_URL + "/request_agent",
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