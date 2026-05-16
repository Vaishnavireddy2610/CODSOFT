import streamlit as st

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 Rule-Based AI Chatbot")

user_input = st.text_input("Ask something:")

if user_input:
    message = user_input.lower()

    if "hello" in message or "hi" in message:
        response = "Hello! Nice to meet you."

    elif "your name" in message:
        response = "I am a Rule-Based AI Chatbot."

    elif "how are you" in message:
        response = "I am functioning properly."

    elif "help" in message:
        response = "You can ask me basic questions like greetings, name, etc."

    elif "bye" in message:
        response = "Goodbye! Have a nice day."

    else:
        response = "Sorry, I don't understand that yet."

    st.success(response)