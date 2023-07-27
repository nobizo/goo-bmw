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
# st.sidebar.markdown("**モデルの選択**")
model = st.sidebar.selectbox("モデル", ["gpt-4","gpt-3.5-turbo"])

# st.sidebar.markdown("**店員の選択**")
clerk = st.sidebar.selectbox("店員", ["リサ", "ケン" ])
clerk_setting = get_clerk_setting(clerk)

# Update the sidebar image based on the clerk selected
clerk_images = {
    "リサ": "BMW_female_concierge.png",
    "ケン": "BMW_male_concierge1.png"
}
st.sidebar.image(clerk_images[clerk])

# Reset Button
if st.sidebar.button("リセット"):
    st.session_state.clear()

# Main interface
st.image("bmw.jpg")

# Display messages
if "messages" in st.session_state:
    for message in st.session_state["messages"]:
        speaker_icon = "🙎" if message["role"] == "user" else "🚗"
        st.write(speaker_icon + ": " + message["content"])

# Input and send button
initial_message = "まずはあなたのニックネームと何をアドバイスしてほしいか教えてください。" if "messages" not in st.session_state else ""
col1, col2 = st.columns([6,1])
user_input = col1.text_area("", value=initial_message, key="user_input")
if col2.button("送信"):
    st.session_state.user_input = user_input
    communicate()
