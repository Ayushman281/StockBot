import os
from google.adk.agents import Agent
from manager.tools.tools import FMPTools

def get_current_price(ticker: str) -> dict:
    """
    Fetch the current price for the given ticker.
    Returns a dict with status and current_price.
    """
    print(f"--- Tool: get_current_price called for {ticker} ---")
    fmp_tools = FMPTools()
    try:
        result = fmp_tools.get_historical_prices(ticker, 1)
        if result["status"] == "error":
            return {
                "status": "error",
                "error": f"Failed to fetch price for {ticker}: {result['error']}"
            }
        data = result["data"]
        if not data or "historical" not in data or not data["historical"]:
            return {
                "status": "error",
                "error": f"No price data available for {ticker}"
            }
        try:
            current_price = float(data["historical"][0]["close"])
        except (KeyError, ValueError, TypeError):
            return {
                "status": "error",
                "error": f"Could not parse current price for {ticker}"
            }
        return {
            "status": "success",
            "ticker": ticker,
            "current_price": current_price
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error fetching price for {ticker}: {str(e)}"
        }

ticker_price = Agent(
    name="ticker_price",
    model="gemini-2.0-flash",
    description="Agent to fetch the current stock price for a given ticker symbol.",
    instruction="""
    You are a specialized agent that fetches the current stock price for a given ticker symbol.
    When given a ticker, call get_current_price(ticker="[SYMBOL]") and return the result.
    """,
    tools=[get_current_price],
)