# Stock Analysis Multi-Agent System

A comprehensive multi-agent system built with Google ADK for analyzing stocks through natural language queries. This system retrieves real-time price data and news to provide intelligent stock analysis with minimal user effort.

## Features

- **Natural Language Processing**: Ask questions in plain English about any stock
- **Multi-Agent Architecture**: Modular design with specialized agents for different tasks
- **Multiple Data Sources**: Integration with Financial Modeling Prep API and NewsAPI
- **Real-time Data**: Live stock prices and recent news analysis
- **Sentiment Analysis**: News sentiment scoring on a 0-10 scale
- **Comprehensive Analysis**: Correlates price movements with news events
- **Resilient Design**: Fallback mechanisms when primary data sources are unavailable

## Example Queries

- "Why did Tesla stock drop today?"
- "What's happening with Palantir stock recently?"
- "How has Nvidia stock changed in the last 7 days?"
- "What's the current price of Apple stock?"
- "Show me recent news about Microsoft"

## Output Format

The system provides standardized analysis output:

```
STOCK ANALYSIS: [TICKER]

Current Price: $[PRICE]
Change: [CHANGE] ([PERCENT]%)
Sentiment Score: [0-10 scale]

Analysis:
[Detailed explanation of price movement and correlation with news]

Recent News:
- [Key news item 1]
- [Key news item 2]
- [Key news item 3]
```

## Architecture

The system consists of 5 specialized sub-agents:

1. **identify_ticker**: Extracts stock ticker symbols from natural language queries
2. **ticker_news**: Retrieves recent news articles about stocks from NewsAPI and FMP
3. **ticker_price**: Fetches current stock prices and trading data
4. **ticker_price_change**: Calculates price changes over different timeframes
5. **ticker_analysis**: Analyzes price movements using news sentiment and historical data

### Data Flow

1. User query → identify_ticker → Extract ticker symbol
2. Manager coordinates parallel data collection:
   - Price data from FMP API
   - Historical prices for change calculation
   - News articles from NewsAPI with FMP fallback
3. Analysis agent correlates price movements with news sentiment
4. Manager compiles final response with standardized format

## Setup

### Prerequisites

- Python 3.8+
- Google ADK installed (`pip install -U google-adk`)
- API keys for:
  - Google Generative AI (Gemini)
  - Financial Modeling Prep API
  - NewsAPI

### Installation

1. Clone this repository
2. Create a `.env` file in the project directory with your API keys:
```
GOOGLE_API_KEY=your_gemini_api_key_here
FMP_API_KEY=your_financial_modeling_prep_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```
3. Navigate to the project directory:
```
cd stock-analysis-system
```
4. Run the application:
```
adk web
```
5. Open your browser to http://localhost:8000

## Data Sources

- **Financial Modeling Prep API**: https://financialmodelingprep.com/developer/docs/
- **NewsAPI**: https://newsapi.org/docs