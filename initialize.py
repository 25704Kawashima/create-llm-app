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

# 環境変数の読み込み
load_dotenv()

# OpenAIとSerpAPIのキーを取得
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SERP_API_KEY = os.getenv('SERP_API_KEY')

# OpenAIのLLMモデルを初期化
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=1, streaming=True)