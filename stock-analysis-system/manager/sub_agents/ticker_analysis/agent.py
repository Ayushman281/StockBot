from google.adk.agents import Agent
from typing import Dict, Any, Union
import logging

print("Loading ticker_analysis module...")

def analyze_stock_movement(ticker: str, price_data: str, news_data: Union[str, None] = None, timeframe: str = "recent") -> dict:
    """
    Analyze stock movement using price and news data
    
    Args:
        ticker: Stock ticker symbol
        price_data: Price change information
        news_data: Recent news about the stock (can be None)
        timeframe: Analysis timeframe
        
    Returns:
        Dictionary with analysis
    """
    print(f"[DEBUG] analyze_stock_movement called for {ticker}")
    
    try:
        # Extract sentiment indicators from news
        positive_keywords = [
            'growth', 'profit', 'beat', 'strong', 'positive', 'up', 'gain', 'bull',
            'revenue', 'earnings', 'expansion', 'success', 'outperform', 'upgrade',
            'buy', 'optimistic', 'record', 'milestone', 'breakthrough'
        ]
        
        negative_keywords = [
            'loss', 'decline', 'weak', 'negative', 'down', 'fall', 'bear', 'concern',
            'miss', 'disappointing', 'cut', 'downgrade', 'sell', 'pessimistic',
            'lawsuit', 'investigation', 'scandal', 'crisis', 'warning', 'risk'
        ]
        
        # Analyze news sentiment - safely handle None
        if news_data is None:
            news_lower = ""
            print("[DEBUG] No news data provided for analysis")
        else:
            news_lower = news_data.lower()
            
        positive_count = sum(1 for word in positive_keywords if word in news_lower)
        negative_count = sum(1 for word in negative_keywords if word in news_lower)
        
        if positive_count > negative_count:
            news_sentiment = "positive"
        elif negative_count > positive_count:
            news_sentiment = "negative"
        else:
            news_sentiment = "neutral"
        
        # Determine price movement direction
        if "increased" in price_data.lower():
            price_direction = "upward"
        elif "decreased" in price_data.lower():
            price_direction = "downward"
        else:
            price_direction = "sideways"
            
        # Generate analysis based on correlation
        if price_direction == "upward" and news_sentiment == "positive":
            correlation = "aligned"
            explanation = "The positive news sentiment aligns with the stock's upward movement, suggesting the market is responding favorably to recent developments."
        elif price_direction == "downward" and news_sentiment == "negative":
            correlation = "aligned"
            explanation = "The negative news sentiment correlates with the stock's decline, indicating market concerns about recent events or fundamentals."
        elif price_direction == "upward" and news_sentiment == "negative":
            correlation = "contrarian"
            explanation = "Despite negative news, the stock is rising. This could indicate oversold conditions, contrarian buying, or other market factors outweighing the news."
        elif price_direction == "downward" and news_sentiment == "positive":
            correlation = "contrarian"
            explanation = "Despite positive news, the stock is declining. This might suggest broader market pressures, profit-taking, or that positive news was already priced in."
        else:
            correlation = "neutral"
            explanation = "Analysis unavailable"
        
        print(f"[DEBUG] Analysis completed for {ticker}")
        
        return {
            "status": "success",
            "ticker": ticker,
            "price_direction": price_direction,
            "news_sentiment": news_sentiment,
            "correlation": correlation,
            "explanation": explanation,
            "timeframe": timeframe
        }
        
    except Exception as e:
        print(f"[ERROR] Error in analyze_stock_movement: {str(e)}")
        return {
            "status": "error",
            "error": f"Error analyzing stock movement for {ticker}: {str(e)}"
        }

ticker_analysis = Agent(
    name="ticker_analysis",
    model="gemini-2.0-flash",
    description="Agent to analyze stock movements using news and price data",
    instruction="""
    You are a specialized agent that analyzes stock movements by correlating price data with news sentiment.
    
    When given ticker, price_data, and news_data parameters:
    1. Print "STARTING ANALYSIS FOR [TICKER]"
    2. Call analyze_stock_movement with the EXACT parameters provided:
       - ticker: The stock symbol (e.g., "TSLA")
       - price_data: String containing price information
       - news_data: String containing news information (may be None)
       - timeframe: Use "recent" if not specified
    3. Present the correlation between price movement and news
    4. Provide clear explanation of likely reasons for the stock movement
    5. Print "COMPLETED ANALYSIS FOR [TICKER]"
    
    Example:
    - When called with ticker="TSLA", price_data="stock decreased by 2.5%", news_data="Negative earnings report"
    - Call analyze_stock_movement(ticker="TSLA", price_data="stock decreased by 2.5%", news_data="Negative earnings report")
    """,
    tools=[analyze_stock_movement],
)

print(f"Initialized ticker_analysis agent")