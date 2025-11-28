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


def ask_ai_agent(question):
    """LLMを使用して質問に回答する"""
    try:
        # プロンプトを生成
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("あなたは有能なアシスタントです。"),
            HumanMessagePromptTemplate.from_template(question),
        ]).format_messages()

        # LLMで応答を生成
        response = init.llm.generate([prompt])["generations"][0][0]["text"]
        return response
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

def handle_user_input(user_input):
    """ユーザー入力に応じて適切な処理を実行する"""
    if "ニュース" in user_input:
        news_data = func.get_news("latest news")
        if 'news_results' in news_data:
            st.header("最新のニュース")
            for article in news_data['news_results']:
                title = article.get('title', 'タイトルなし')
                snippet = article.get('snippet', '説明なし')
                link = article.get('link', '#')
                st.subheader(title)
                st.write(snippet)
                st.write(f"[リンク]({link})")
        elif 'error' in news_data:
            st.error(news_data['error'])
        else:
            st.error("ニュースを取得できませんでした。")
    elif "日経" in user_input or "株価" in user_input:
        stock_price = func.get_nikkei_stock_price()
        if stock_price:
            st.header("日経平均株価")
            st.write(f"現在の終値: {stock_price} 円")
        else:
            st.error("日経平均株価を取得できませんでした。")
    else:
        response = ask_ai_agent(user_input)
        st.header("AIエージェントの回答")
        st.write(response)

# Streamlit アプリのレイアウト
st.title("ニュースと日経平均株価エージェント")

user_input = st.text_input("質問やリクエストを入力してください:")
if st.button('送信'):
    if user_input:
        handle_user_input(user_input)
    else:
        st.error("入力が空です。")