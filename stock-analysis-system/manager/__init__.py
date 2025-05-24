"""
Stock Analysis System Manager
This module initializes the main agent and ensures all sub-agents are properly loaded
"""

print("Loading manager module...")

# Import the main agent - it will handle subagent imports
from .agent import agent

# Export the agent
__all__ = ['agent']

print("Manager module loaded successfully")