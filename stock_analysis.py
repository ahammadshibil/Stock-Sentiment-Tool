import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import yfinance as yf

def get_stock_data(stock_symbol):
    stock_info = yf.Ticker(stock_symbol).info

    stock_data = {}
    stock_data["symbol"] = stock_symbol
    stock_data["name"] = stock_info["shortName"]
    
    if "regularMarketPrice" in stock_info:
        stock_data["price"] = stock_info["regularMarketPrice"]
    elif "regularMarketPreviousClose" in stock_info:
        stock_data["price"] = stock_info["regularMarketPreviousClose"]
    else:
        stock_data["price"] = None
    
    if "regularMarketChange" in stock_info:
        stock_data["change"] = stock_info["regularMarketChange"]
    else:
        stock_data["change"] = None

    return stock_data



# Functions for stock data, summary, and fundamental data
def get_stock_summary(stock_symbol):
    stock_info = yf.Ticker(stock_symbol).info
    summary = f"{stock_info['longBusinessSummary'][:500]}..."
    return summary

def get_fundamental_data(stock_symbol):
    stock_info = yf.Ticker(stock_symbol).info

    market_cap = stock_info.get('marketCap', None)
    trailing_pe = stock_info.get('trailingPE', None)
    forward_pe = stock_info.get('forwardPE', None)
    peg_ratio = stock_info.get('pegRatio', None)
    dividend_yield = stock_info.get('dividendYield', None)

    fundamental_data = {
        'Market Cap': market_cap,
        'Trailing P/E': trailing_pe,
        'Forward P/E': forward_pe,
        'PEG Ratio': peg_ratio,
        'Dividend Yield': dividend_yield
    }

    return fundamental_data

# ... (same as before)

# Functions for sentiment analysis using VADER
def get_news_headlines(stock_symbol):
    base_url = "https://www.bing.com/news/search?q={}&format=rss"
    url = base_url.format(stock_symbol)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")
    headlines = [item.title.text for item in soup.find_all("item")]
    return headlines
    # ... (same as before)

def analyze_sentiment_vader(headlines):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = []

    for headline in headlines:
        sentiment_score = analyzer.polarity_scores(headline)
        compound_score = sentiment_score["compound"]

        if compound_score >= 0.05:
            sentiment_scores.append("positive")
        elif compound_score <= -0.05:
            sentiment_scores.append("negative")
        else:
            sentiment_scores.append("neutral")

    return sentiment_scores

stock_symbol = input("Enter the stock symbol you want to analyze: ")

stock_data = get_stock_data(stock_symbol)
stock_summary = get_stock_summary(stock_symbol)
fundamental_data = get_fundamental_data(stock_symbol)

# Sentiment analysis
headlines = get_news_headlines(stock_symbol)
sentiment_scores = analyze_sentiment_vader(headlines)

positive_count = sentiment_scores.count("positive")
negative_count = sentiment_scores.count("negative")
neutral_count = sentiment_scores.count("neutral")

print(f"Stock Data: {stock_data}")
print(f"Stock Summary: {stock_summary}")
print("Fundamental Data:")
for key, value in fundamental_data.items():
    print(f"{key}: {value}")

print(f"Sentiment Analysis:")
print(f"Positive headlines: {positive_count}")
print(f"Negative headlines: {negative_count}")
print(f"Neutral headlines: {neutral_count}")
