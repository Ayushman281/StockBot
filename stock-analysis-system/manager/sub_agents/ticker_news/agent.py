import os
import sys
from google.adk.agents import Agent
from manager.tools.tools import FMPTools

def get_ticker_news(ticker: str, limit: int = 5) -> dict:
    """
    Get recent news for a stock ticker
    
    Args:
        ticker: Stock ticker symbol
        limit: Number of news articles to retrieve
        
    Returns:
        Dictionary with news information
    """
    print(f"--- Tool: get_ticker_news called for ticker: {ticker} ---")
    
    fmp_tools = FMPTools()
    
    try:
        news_result = fmp_tools.get_stock_news(ticker, limit)
        
        if news_result["status"] == "error":
            return {
                "status": "error",
                "error": f"Failed to fetch news for {ticker}: {news_result['error']}"
            }
        
        news_data = news_result["data"]
        
        if not news_data:
            return {
                "status": "success",
                "ticker": ticker,
                "news": f"No recent news found for {ticker}"
            }
        
        formatted_news = []
        for article in news_data[:limit]:
            formatted_news.append({
                "title": article.get('title', 'No title'),
                "summary": article.get('text', '')[:200] + "..." if article.get('text') else 'No summary',
                "published": article.get('publishedDate', 'Unknown date'),
                "url": article.get('url', '')
            })
        
        return {
            "status": "success",
            "ticker": ticker,
            "news": formatted_news,
            "count": len(formatted_news)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error retrieving news for {ticker}: {str(e)}"
        }

ticker_news = Agent(
    name="ticker_news",
    model="gemini-2.0-flash",
    description="Agent to retrieve recent news about a stock ticker",
    instruction="""
    You are a specialized agent that retrieves and summarizes recent news for stock tickers.
    
    When asked for news about a stock:
    1. Use the get_ticker_news tool to fetch recent articles
    2. Present the news in a clear, organized format
    3. Include article titles, summaries, and publication dates
    4. If no news is found, inform the user appropriately
    """,
    tools=[get_ticker_news],
)