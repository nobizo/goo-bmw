import streamlit as st
import openai

def get_clerk_setting(clerk):
    clerk_settings = {
        "リサ": "The assistant is a 23-year-old woman who speaks Kansai-ben, a dialect of Japanese. Her name is Sayuri.",
        "ケン": "The assistant is a 35-year-old man who speaks kyoto-ben, a dialect of Japanese. His name is Kenji.",
    }
    return clerk_settings.get(clerk)

def communicate():
    messages = st.session_state.get("messages", [])
    
    # Add system message based on clerk's setting
    if not messages:
        messages.append({"role": "system", "content": get_clerk_setting(clerk)})

    user_message = {"role": "user", "content": st.session_state.user_input}    
    messages.append(user_message)
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    
    bot_message = response["choices"][0]["message"]
    messages.append({"role": "assistant", "content": bot_message["content"]})
    st.session_state.messages = messages  # Update the session state with modified messages

# Set API keys
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# Sidebar configurations
st.sidebar.markdown("**モデルの選択**")
model = st.sidebar.selectbox("
