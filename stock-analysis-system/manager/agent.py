from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
import sys
import logging

# Set up basic logging at the beginning
print("==========================================")
print("STOCK ANALYSIS SYSTEM STARTING")
print("==========================================")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - StockBot: %(message)s')
print(f"Python version: {sys.version}")
print("Loading manager agent...")

# Use relative imports with dot notation
from .sub_agents.identify_ticker.agent import identify_ticker
from .sub_agents.ticker_news.agent import ticker_news
from .sub_agents.ticker_price.agent import ticker_price
from .sub_agents.ticker_price_change.agent import ticker_price_change
from .sub_agents.ticker_analysis.agent import ticker_analysis

print(f"All sub-agents loaded successfully")

agent = Agent(
    name="stock_analysis_manager",
    model="gemini-2.0-flash",
    description="Multi-agent system for comprehensive stock analysis",
    instruction="""
    You are a stock analysis manager coordinating multiple agents for stock market insights.
    
    IMMEDIATE ACTION REQUIRED:
    
    1. For ANY stock-related question, print "WORKFLOW STARTED: IDENTIFYING TICKER" and use the identify_ticker agent by calling transfer_to_agent with agent_name="identify_ticker".
    
    2. When identify_ticker returns control to you with a ticker identified, print "TICKER IDENTIFIED: [SYMBOL]" and IMMEDIATELY:
       a. Print "STEP 1: GETTING PRICE DATA" and call ticker_price with request="get price for [SYMBOL]"
       b. Print "STEP 2: GETTING PRICE CHANGE" and call ticker_price_change with request="calculate 1day change for [SYMBOL]"
       c. Print "STEP 3: GETTING NEWS DATA" and call ticker_news with request="get news for [SYMBOL]"
       d. Print "STEP 4: ANALYZING DATA" and call ticker_analysis with request="analyze [SYMBOL] movement based on price and news data"
    
    3. You MUST complete ALL steps in sequence without stopping.
    
    4. After completing all steps, provide a comprehensive response. It must include:
    - The identified ticker symbol
    - The current price
    - The last recoprded price in the timeframe requested
    - The price change in the timeframe requested (e.g., 1 day, 1 week)
    - The price change percentage
    - The latest news headlines
    - The analysis of the stock movement based on price and news data
    - A clear explanation of the likely reasons for the stock movement

    
    IMPORTANT: When control returns from identify_ticker, IMMEDIATELY begin the analysis workflow.
    
    Example:
    - If identify_ticker identifies TSLA, call ticker_price with request="get price for TSLA"
    - Then call ticker_price_change with request="calculate 1day change for TSLA"
    - Then call ticker_news with request="get news for TSLA"
    - Then call ticker_analysis with request="analyze TSLA movement based on price and news data"
    """,
    sub_agents=[identify_ticker],
    tools=[
        AgentTool(ticker_price),
        AgentTool(ticker_news),
        AgentTool(ticker_price_change),
        AgentTool(ticker_analysis),
    ],
)

print(f"Manager agent '{agent.name}' initialized successfully with {len(agent.tools)} tools")
print("==========================================")
print("STOCK ANALYSIS SYSTEM READY")
print("==========================================")