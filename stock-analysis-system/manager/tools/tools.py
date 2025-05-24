import requests
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

class FMPTools:
    def __init__(self):
        self.api_key = os.getenv('FMP_API_KEY')
        self.base_url = 'https://financialmodelingprep.com/api/v3'
    
    def get_stock_quote(self, symbol: str) -> dict:
        """Get current stock quote"""
        url = f"{self.base_url}/quote/{symbol}"
        params = {'apikey': self.api_key}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return {"status": "success", "data": data}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_historical_prices(self, symbol: str, days: int = 30) -> dict:
        """Get historical price data"""
        url = f"{self.base_url}/historical-price-full/{symbol}"
        params = {
            'apikey': self.api_key,
            'timeseries': days
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return {"status": "success", "data": data}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_stock_news(self, symbol: str, limit: int = 10) -> dict:
        """Get news for a specific stock"""
        # Try to use NewsAPI first
        news_api_result = self._get_news_from_newsapi(symbol, limit)
        if news_api_result["status"] == "success" and news_api_result["data"]:
            return news_api_result
        
        # Fall back to FMP if NewsAPI fails
        url = f"{self.base_url}/stock_news"
        params = {
            'tickers': symbol,
            'limit': limit,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return {"status": "success", "data": data}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _get_news_from_newsapi(self, symbol: str, limit: int = 10) -> dict:
        """Get news from NewsAPI as a backup/alternative source"""
        news_api_key = os.getenv('NEWS_API_KEY')
        if not news_api_key:
            return {"status": "error", "error": "NEWS_API_KEY not found in environment variables"}
        
        # Calculate date range for last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        from_date = start_date.strftime("%Y-%m-%d")
        to_date = end_date.strftime("%Y-%m-%d")
        
        # Create search query for better results
        query = f"{symbol} stock OR {symbol} shares OR {symbol} company"
        
        # NewsAPI endpoint
        url = "https://newsapi.org/v2/everything"
        
        params = {
            "q": query,
            "from": from_date,
            "to": to_date,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": limit,
            "apiKey": news_api_key
        }
        
        try:
            print(f"--- Attempting to fetch news for {symbol} from NewsAPI ---")
            response = requests.get(url, params=params)
            response.raise_for_status()
            news_data = response.json()
            
            # Check if we got valid data
            if news_data.get("status") == "ok" and news_data.get("articles"):
                # Convert to a format similar to FMP for consistency
                formatted_articles = []
                
                for article in news_data["articles"]:
                    formatted_articles.append({
                        "title": article.get("title", "No title"),
                        "text": article.get("description", "") + "\n\n" + article.get("content", ""),
                        "publishedDate": article.get("publishedAt", "Unknown date"),
                        "url": article.get("url", ""),
                        "source": article.get("source", {}).get("name", "Unknown source"),
                        "image": article.get("urlToImage", "")
                    })
                
                print(f"--- Successfully retrieved {len(formatted_articles)} articles from NewsAPI ---")
                return {"status": "success", "data": formatted_articles}
            else:
                print(f"--- No articles found on NewsAPI for {symbol} ---")
                return {"status": "error", "error": f"No news found for {symbol} on NewsAPI"}
                
        except Exception as e:
            print(f"--- NewsAPI error: {str(e)} ---")
            return {"status": "error", "error": f"NewsAPI error: {str(e)}"}
    
    def search_symbol(self, query: str) -> dict:
        """Search for stock symbols"""
        url = f"{self.base_url}/search"
        params = {
            'query': query,
            'limit': 10,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return {"status": "success", "data": data}
        except Exception as e:
            return {"status": "error", "error": str(e)}