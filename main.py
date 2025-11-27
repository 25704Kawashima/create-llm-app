from dotenv import load_dotenv
import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv()
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5,streaming=True)

st.title("LLMチャットアプリ")

selected_chat = st.radio(
    "チャットを選択してください", 
    ("システムエンジニア", "歴史の専門家")
)

st.divider()


input_message = st.text_input(label=f"{selected_chat}への質問を入力してください:")

system_template = "あなたは{expert}です。質問に対してわかりやすく丁寧に答えてください。また、専門分野外の質問には答えず、その旨を伝えてください。"
human_template = "{input}"

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template(human_template),
])

if st.button("送信"):
    st.divider()

    messages = prompt.format_messages(expert=selected_chat,input=input_message)
    result = llm(messages)
    st.write("### 回答:")
    st.write(result.content)