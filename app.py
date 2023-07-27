import streamlit as st
import openai

def communicate():
    messages = st.session_state.get("messages", [])
    
    # Add system message based on nickname
    if not messages and "nickname" in st.session_state:
        greeting = f"こんにちは、{st.session_state['nickname']}さん。"
        messages.append({"role": "system", "content": greeting})

    user_message = {"role": "user", "content": st.session_state["user_input"]}    
    messages.append(user_message)
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    
    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)
    st.session_state["user_input"] = ""
    st.session_state["messages"] = messages  # Update the session state with modified messages

# Set API keys
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# Sidebar configurations
st.sidebar.image("goo-net2.png")
model = "gpt-4"
clerk = "リサ"

clerk_images = {
    "リサ": "BMW_female_concierge.png",
    "ケン": "BMW_male_concierge1.png"
}
st.sidebar.image(clerk_images[clerk])

# Add input for nickname and set button
nickname = st.sidebar.text_input("ニックネームを入力:")
if st.sidebar.button("設定"):
    st.session_state["nickname"] = nickname
    communicate()  

# Reset Button
if st.sidebar.button("リセット"):
    st.session_state.clear()

# Main interface
st.image("bmw.jpg")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# CSS を Streamlit アプリに埋め込む
user_input = st.text_area("", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    for message in reversed(st.session_state["messages"]):
        speaker_icon = "🙎" if message["role"] == "user" else "🚗"
        st.write(speaker_icon + ": " + message["content"])
