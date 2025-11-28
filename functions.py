# 関数群をまとめたファイル
import streamlit as st
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import requests
import initialize as init
import xml.etree.ElementTree as ET

def get_news(query):
    """SerpAPIを使用して日本のニュースを取得する"""
    url = 'https://serpapi.com/search'
    params = {
        'engine': 'google_news',
        'q': query,
        'api_key': init.SERP_API_KEY,
        'gl': 'jp',  # 日本の地域に限定
        'hl': 'ja',  # 日本語のニュースに限定
        'num': 10,    # 取得するニュースの数
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
        'api_key': init.SERP_API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'markets' in data and 'asia' in data['markets']:
            for market in data['markets']['asia']:
                if market.get('name') == 'Nikkei 225':
                    return market.get('price')
        return "日経平均株価のデータが見つかりませんでした。"
    else:
        return f"HTTPエラー: {response.status_code}"
    
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

def get_yahoo_news():
    """Yahoo! JAPANのRSSフィードからニュースを取得する"""
    url = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"  # Yahoo! JAPANのトップニュースRSS
    response = requests.get(url)
    if response.status_code == 200:
        # XMLをパース
        root = ET.fromstring(response.content)
        news_items = []
        for item in root.findall(".//item"):
            title = item.find("title").text
            link = item.find("link").text
            description = item.find("description").text if item.find("description") is not None else "説明なし"
            news_items.append({"title": title, "link": link, "description": description})
        return news_items
    else:
        return {"error": f"HTTP {response.status_code}: ニュースを取得できませんでした。"}

def handle_user_input(user_input):
    """ユーザー入力に応じて適切な処理を実行する"""
    if "ニュース" in user_input:
        news_data = get_news("latest news")
        if 'news_results' in news_data:
            st.header("最新のニュース")
            for i, article in enumerate(news_data['news_results']):
                if i >= 10:  # 最大10回でループを終了
                    break
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
        stock_price = get_nikkei_stock_price()
        if stock_price:
            st.header("日経平均株価")
            st.write(f"現在の終値: {stock_price} 円")
        else:
            st.error("日経平均株価を取得できませんでした。")
    else:
        response = ask_ai_agent(user_input)
        st.header("AIエージェントの回答")
        st.write(response)
