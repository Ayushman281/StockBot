import re
import os
import sys
from google.adk.agents import Agent
from manager.tools.tools import FMPTools
import logging

def identify_ticker_from_query(query: str) -> dict:
    """
    Identify stock ticker from user query
    
    Args:
        query: User's natural language query about a stock
        
    Returns:
        Dictionary with ticker information
    """
    print(f"[DEBUG] identify_ticker_from_query called for query: {query}")
    
    fmp_tools = FMPTools()
    query_lower = query.lower()
    
    # Common company name to ticker mappings
    ticker_map = {
        'tesla': 'TSLA',
        'apple': 'AAPL',
        'microsoft': 'MSFT',
        'google': 'GOOGL',
        'alphabet': 'GOOGL',
        'amazon': 'AMZN',
        'meta': 'META',
        'facebook': 'META',
        'nvidia': 'NVDA',
        'palantir': 'PLTR',
        'netflix': 'NFLX',
        'spotify': 'SPOT',
        'uber': 'UBER',
        'lyft': 'LYFT',
        'airbnb': 'ABNB'
    }
    
    # First, check for direct ticker mentions (2-5 uppercase letters)
    ticker_pattern = r'\b[A-Z]{2,5}\b'
    direct_tickers = re.findall(ticker_pattern, query)
    if direct_tickers:
        result = {
            "status": "success",
            "ticker": direct_tickers[0],
            "method": "direct_match"
        }
        print(f"[DEBUG] Identified ticker: {result['ticker']} via {result['method']}")
        return result
    
    # Check our predefined mapping
    for company, ticker in ticker_map.items():
        if company in query_lower:
            result = {
                "status": "success",
                "ticker": ticker,
                "method": "company_name_match"
            }
            print(f"[DEBUG] Identified ticker: {result['ticker']} via {result['method']}")
            return result
    
    # Extract potential company names and search via API
    words = query_lower.split()
    for word in words:
        if len(word) > 3 and word not in ['stock', 'price', 'why', 'what', 'how', 'today', 'recently']:
            search_result = fmp_tools.search_symbol(word)
            if search_result["status"] == "success" and search_result["data"]:
                result = {
                    "status": "success",
                    "ticker": search_result["data"][0]["symbol"],
                    "method": "api_search"
                }
                print(f"[DEBUG] Identified ticker: {result['ticker']} via {result['method']}")
                return result
    
    print("[DEBUG] No ticker found")
    return {
        "status": "error",
        "error": "TICKER_NOT_FOUND"
    }

identify_ticker = Agent(
    name="identify_ticker",
    model="gemini-2.0-flash",
    description="Agent to identify stock ticker symbols from natural language queries",
    instruction="""
    You are a specialized agent that identifies stock ticker symbols from user queries.
    
    CRITICAL WORKFLOW:
    1. Print: "PROCESSING QUERY TO IDENTIFY TICKER"
    2. Use the identify_ticker_from_query tool to extract the ticker symbol
    3. When you find a ticker, print: "FOUND TICKER: [TICKER_SYMBOL]" 
    4. IMMEDIATELY call transfer_to_agent(agent_name="stock_analysis_manager") without ANY other text
    
    Your ONLY response should be:
    1. "PROCESSING QUERY TO IDENTIFY TICKER"
    2. Call identify_ticker_from_query
    3. "FOUND TICKER: XXXX"
    4. Call transfer_to_agent
    
    DO NOT add any additional text, explanations, or responses.
    DO NOT acknowledge or answer the user's question directly.
    ALWAYS transfer control back to stock_analysis_manager immediately after printing the ticker.
    """,
    tools=[identify_ticker_from_query],
)

print(f"Initialized {identify_ticker.name} agent")