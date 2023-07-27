import streamlit as st
import openai
# from gtts import gTTS

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
# st.sidebar.markdown("**モデルの選択**")
# model = st.sidebar.selectbox("モデル", ["gpt-3.5-turbo", "gpt-4"])
model = "gpt-4"


# Update the sidebar image based on the clerk selected
clerk_images = {
    "リサ": "BMW_female_concierge.png",
    "ケン": "BMW_male_concierge1.png"
}
st.sidebar.image(clerk_images[clerk])

# st.sidebar.markdown("**店員の選択**")
clerk = st.sidebar.selectbox("", ["リサ", "ケン" ])
clerk_setting = get_clerk_setting(clerk)

# Reset Button
if st.sidebar.button("リセット"):
    st.session_state.clear()

# Main interface
st.image("bmw.jpg")
# st.write(f"{clerk}です。わたしはあなたのライフスタイルにあったクルマ探しのお手伝いをします。")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": st.secrets.AppSettings.chatbot_setting}]

user_input = st.text_input("まずはあなたのニックネームと何をアドバイスしてほしいか教えてください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    for message in reversed(st.session_state["messages"][1:]):
        speaker_icon = "🙎" if message["role"] == "user" else "🚗"
        st.write(speaker_icon + ": " + message["content"])
        
#        text = message["content"]
#        tts = gTTS(text, lang='ja')
#        tts.save('welcome.mp3')
#        st.audio('welcome.mp3')
