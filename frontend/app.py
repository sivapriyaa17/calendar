import streamlit as st
import requests

st.set_page_config(page_title="Calendar Assistant", page_icon="📅")

st.title(" Google Calendar Booking Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask me to schedule a meeting...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        print("Sending to backend:", {"message": user_input})
        res = requests.post("https://calendar-1-ouhh.onrender.com/chat", json={"message": user_input})
        print("📤 Sent to backend:", {"message": user_input})
        bot_reply = res.json().get("response", "Something went wrong.")
        st.markdown(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
