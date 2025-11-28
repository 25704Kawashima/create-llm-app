from dotenv import load_dotenv
import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import requests
import functions as func
import initialize as init

init.load_dotenv()

# Streamlit アプリのレイアウト
st.title("ニュースと日経平均株価エージェント")

user_input = st.text_input("質問やリクエストを入力してください:")
if st.button('送信'):
    if user_input:
        func.handle_user_input(user_input)
    else:
        st.error("入力が空です。")