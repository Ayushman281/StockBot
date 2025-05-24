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