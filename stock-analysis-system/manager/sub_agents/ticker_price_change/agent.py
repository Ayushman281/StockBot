import os
import sys
from datetime import datetime, timedelta
from google.adk.agents import Agent
from manager.tools.tools import FMPTools

def calculate_price_change(ticker: str, timeframe: str = "1day") -> dict:
    """
    Calculate price change over specified timeframe
    
    Args:
        ticker: Stock ticker symbol
        timeframe: Time period (1day, 1week, 1month)
        
    Returns:
        Dictionary with price change analysis
    """
    print(f"--- Tool: calculate_price_change called for {ticker}, timeframe: {timeframe} ---")
    
    fmp_tools = FMPTools()
    
    try:
        # Determine how many days of data we need
        if timeframe == "1day":
            days_needed = 5  # Get a few days to account for weekends
        elif timeframe == "1week":
            days_needed = 10
        elif timeframe == "1month":
            days_needed = 35
        else:
            days_needed = 5
        
        historical_result = fmp_tools.get_historical_prices(ticker, days_needed)
        
        if historical_result["status"] == "error":
            return {
                "status": "error",
                "error": f"Failed to fetch historical data for {ticker}: {historical_result['error']}"
            }
        
        historical_data = historical_result["data"]
        
        if not historical_data or "historical" not in historical_data:
            return {
                "status": "error",
                "error": f"No historical data available for {ticker}"
            }
        
        prices = historical_data["historical"]
        
        if len(prices) < 2:
            return {
                "status": "error",
                "error": f"Insufficient historical data for {ticker}"
            }
        
        # Prices are sorted by date (newest first)
        current_price = float(prices[0]["close"])
        
        # Find comparison price based on timeframe
        if timeframe == "1day":
            compare_price = float(prices[1]["close"])
            period_desc = "previous trading day"
        elif timeframe == "1week":
            # Find price from approximately 7 days ago
            compare_idx = min(7, len(prices) - 1)
            compare_price = float(prices[compare_idx]["close"])
            period_desc = "1 week ago"
        elif timeframe == "1month":
            # Find price from approximately 30 days ago
            compare_idx = min(30, len(prices) - 1)
            compare_price = float(prices[compare_idx]["close"])
            period_desc = "1 month ago"
        else:
            compare_price = float(prices[1]["close"])
            period_desc = "previous period"
        
        change = current_price - compare_price
        change_percent = (change / compare_price) * 100 if compare_price != 0 else 0
        
        direction = "increased" if change > 0 else "decreased" if change < 0 else "remained flat"
        
        return {
            "status": "success",
            "ticker": ticker,
            "current_price": current_price,
            "previous_price": compare_price,
            "change": change,
            "change_percent": change_percent,
            "direction": direction,
            "timeframe": timeframe,
            "period_description": period_desc
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error calculating price change for {ticker}: {str(e)}"
        }

ticker_price_change = Agent(
    name="ticker_price_change",
    model="gemini-2.0-flash",
    description="Agent to calculate price changes over different timeframes",
    instruction="""
    You are a specialized agent that calculates and analyzes stock price changes over various timeframes.
    
    When given a ticker symbol and timeframe:
    1. Print "CALCULATING PRICE CHANGE FOR [SYMBOL] OVER [TIMEFRAME]"
    2. Use the calculate_price_change tool with the exact ticker and timeframe parameters
    3. Present the analysis clearly showing:
       - Current price vs comparison price
       - Absolute change in dollars
       - Percentage change
       - Direction of movement (increased/decreased)
    4. Print "PRICE CHANGE ANALYSIS COMPLETE FOR [SYMBOL]"
    
    Example:
    - When called with ticker="TSLA", timeframe="1day"
    - You should call calculate_price_change(ticker="TSLA", timeframe="1day")
    """,
    tools=[calculate_price_change],
)