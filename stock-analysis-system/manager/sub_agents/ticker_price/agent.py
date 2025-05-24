import os
import sys
from google.adk.agents import Agent
from manager.tools.tools import FMPTools

def get_current_price(ticker: str) -> dict:
    """
    Get current stock price and basic info
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Dictionary with price information
    """
    print(f"--- Tool: get_current_price called for ticker: {ticker} ---")
    
    fmp_tools = FMPTools()
    
    try:
        quote_result = fmp_tools.get_stock_quote(ticker)
        
        if quote_result["status"] == "error":
            return {
                "status": "error",
                "error": f"Failed to fetch price for {ticker}: {quote_result['error']}"
            }
        
        quote_data = quote_result["data"]
        
        if not quote_data or len(quote_data) == 0:
            return {
                "status": "error",
                "error": f"No price data available for {ticker}"
            }
        
        quote = quote_data[0]  # FMP returns a list
        
        price_info = {
            "status": "success",
            "ticker": ticker,
            "price": quote.get('price', 'N/A'),
            "change": quote.get('change', 'N/A'),
            "change_percent": quote.get('changesPercentage', 'N/A'),
            "day_high": quote.get('dayHigh', 'N/A'),
            "day_low": quote.get('dayLow', 'N/A'),
            "volume": quote.get('volume', 'N/A'),
            "market_cap": quote.get('marketCap', 'N/A'),
            "timestamp": quote.get('timestamp', 'N/A')
        }
        
        return price_info
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error retrieving price for {ticker}: {str(e)}"
        }

# Create a function that accepts 'request' parameter to parse ticker from request
def process_price_request(request: str) -> dict:
    """
    Process a price request string to extract ticker and get price
    
    Args:
        request: Request string like "get price for TSLA"
        
    Returns:
        Dictionary with price information
    """
    print(f"--- Tool: process_price_request called with: {request} ---")
    
    # Extract ticker from request
    parts = request.split()
    ticker = None
    for i, word in enumerate(parts):
        if i > 0 and word.upper() == word and len(word) >= 2 and len(word) <= 5:
            ticker = word
            break
    
    if not ticker:
        # Try to find the last word as ticker
        ticker = parts[-1].upper()
        
    print(f"--- Extracted ticker: {ticker} from request ---")
    
    # Call the original function with extracted ticker
    return get_current_price(ticker)

ticker_price = Agent(
    name="ticker_price",
    model="gemini-2.0-flash",
    description="Agent to get current stock price information",
    instruction="""
    You are a specialized agent that retrieves current stock price information.
    
    When given a request like "get price for [SYMBOL]":
    1. Print "RETRIEVING PRICE DATA FOR [SYMBOL]"
    2. Extract the ticker symbol from the request
    3. Use the process_price_request tool with the exact request
    4. Present the information in a clear, formatted way
    5. Print "PRICE DATA RETRIEVED FOR [SYMBOL]" when complete
    """,
    tools=[process_price_request],
)