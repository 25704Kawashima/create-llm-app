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

def get_news(query):
    """SerpAPIを使用してニュースを取得する"""
    url = 'https://serpapi.com/search'
    params = {
        'engine': 'google_news',
        'q': query,
        'api_key': SERP_API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"HTTP {response.status_code}: ニュースを取得できませんでした。"}

def get_nikkei_stock_price():
    """SerpAPIを使用して日経平均株価を取得する"""
    url = 'https://serpapi.com/search'
    params = {
        'engine': 'google_finance',
        'q': 'Nikkei 225',
        'api_key': SERP_API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # 日経平均株価を`markets`セクションから取得
        if 'markets' in data and 'asia' in data['markets']:
            for market in data['markets']['asia']:
                if market.get('name') == 'Nikkei 225':
                    return market.get('price')
        return None
    else:
        print(f"HTTPエラー: {response.status_code}")
        return None

def ask_ai_agent(question):
    """LLMを使用して質問に回答する"""
    try:
        # プロンプトを生成
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("あなたは有能なアシスタントです。"),
            HumanMessagePromptTemplate.from_template(question),
        ]).format_messages()

        # LLMで応答を生成
        response = llm.generate([prompt])["generations"][0][0]["text"]
        return response
    except Exception as e:
        # エラーが発生した場合にエラーメッセージを返す
        return f"エラーが発生しました: {str(e)}"

# Streamlit アプリのレイアウト
st.title("朝のニュースと日経平均株価アプリ")

# ニュース取得
if st.button('ニュースを取得'):
    news_data = get_news("latest news")
    if 'news_results' in news_data:
        st.header("最新のニュース")
        for article in news_data['news_results']:
            st.subheader(article['title'])
            st.write(article['snippet'])
            st.write(f"[リンク]({article['link']})")
    elif 'error' in news_data:
        st.error(news_data['error'])
    else:
        st.error("ニュースを取得できませんでした。")

# 日経平均株価取得
if st.button('日経平均株価を取得'):
    stock_price = get_nikkei_stock_price()
    if stock_price:
        st.header("日経平均株価")
        st.write(f"現在の終値: {stock_price} 円")
    else:
        st.error("日経平均株価を取得できませんでした。")

# AIエージェントへの質問
question = st.text_input("AIエージェントに質問する:")
if st.button('質問を送信'):
    if question:
        response = ask_ai_agent(question)
        st.header("AIエージェントの回答")
        st.write(response)
    else:
        st.error("質問を入力してください。")