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
import initialize as init

load_dotenv()

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