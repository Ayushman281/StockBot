# Stock Analysis Multi-Agent System

A comprehensive multi-agent system built with Google ADK for analyzing stocks through natural language queries.

## Features

- **Natural Language Processing**: Ask questions in plain English about any stock
- **Multi-Agent Architecture**: Modular design with specialized agents for different tasks
- **Real-time Data**: Live stock prices and recent news via Financial Modeling Prep API
- **Comprehensive Analysis**: Combines price data and news sentiment for insights

## Example Queries

- "Why did Tesla stock drop today?"
- "What's happening with Palantir stock recently?"
- "How has Nvidia stock changed in the last 7 days?"
- "What's the current price of Apple stock?"
- "Show me recent news about Microsoft"

## Architecture

The system consists of 5 specialized sub-agents:

1. **identify_ticker**: Extracts stock ticker symbols from natural language queries
2. **ticker_news**: Retrieves recent news articles about stocks
3. **ticker_price**: Fetches current stock prices and trading data
4. **ticker_price_change**: Calculates price changes over different timeframes
5. **ticker_analysis**: Analyzes price movements using news and historical data

## Setup

1. Add your API keys to the `.env` file
2. Run with `adk web` from the manager directory