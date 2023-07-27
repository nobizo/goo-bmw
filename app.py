import streamlit as st
import openai

def communicate():
    if not st.session_state.get("nickname"):
        st.session_state["nickname"] = st.session_state.get("nickname_temp", "")
    messages = st.session_state.get("messages", [])
    
    # Add system message based on nickname
    if not messages and "nickname" in st.session_state:
        greeting = f"こんにちは、{st.session_state['nickname']}さん。グーネットのBMWコンシェルジュサービスへようこそ！どんなクルマをお探しですか？BMWのことならどんなことでもご質問ください。"
        messages.append({"role": "system", "content": greeting})

    if st.session_state["user_input"].strip():
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

# Set System role
chatbot_system_role = st.secrets.AppSettings.chatbot_setting

# Sidebar configurations
st.sidebar.image("goo-net2.png")
model = "gpt-4"
clerk = "リサ"

clerk_images = {
    "リサ": "BMW_female_concierge.png",
    "ケン": "BMW_male_concierge1.png"
}
st.sidebar.image(clerk_images[clerk])

# Add input for nickname
nickname = st.sidebar.text_input("ニックネームを入力:", key="nickname_temp", on_change=communicate)

# Reset Button
if st.sidebar.button("リセット"):
    keys_to_delete = list(st.session_state.keys())
    for key in keys_to_delete:
        del st.session_state[key]
    st.session_state["nickname_temp"] = ""
    st.experimental_rerun()

# Main interface
st.image("bmw-goo.jpg")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# セッションステートの"user_input"の初期化
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# CSS を Streamlit アプリに埋め込む
if "nickname" in st.session_state:
    user_input = st.text_area("", value=st.session_state["user_input"], key="user_input", on_change=communicate)
else:
    st.text_area("", "ニックネームをサイドバーから設定してください。", disabled=True)

#　user_input = st.text_input("", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    for message in reversed(st.session_state["messages"]):
        speaker_icon = "🙎" if message["role"] == "user" else "🚗"
        st.write(speaker_icon + ": " + message["content"])
