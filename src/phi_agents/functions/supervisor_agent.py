"""Supervisor Agent - Orchestrates and coordinates the agent team.

The supervisor agent acts as the coordinator and decision-maker for the entire
agent team. It:
- Routes queries to appropriate specialist agents
- Synthesizes results from multiple agents
- Ensures consistency and quality of responses
- Provides oversight and final answer formatting
- Manages agent interactions and delegation

Example queries:
- "Compare the latest financial performance of Tesla with weather impact on supply chain"
- "Search for AI news and get analyst recommendations for related companies"
- "Find the best F1 driver for 2024 and explain using latest news and financial data"
"""

import os
import sys
sys.path.append("src/")

from phi_agents.logger import get_logger
logger = get_logger(__name__)

from agno.agent import Agent
from phi_agents.functions.model_factory import get_model_from_config, get_default_model_id

from dotenv import load_dotenv

load_dotenv(".env")


def supervisor_agent(model_id: str = None):
    """Create a supervisor agent that coordinates the specialist agent team.
    
    Args:
        model_id: Model identifier in format 'provider:model_name'.
                 If None, uses default from config.json
    
    Returns:
        Agent instance configured as a supervisor
    """
    if model_id is None:
        model_id = get_default_model_id()
    
    logger.debug(f"Initializing Supervisor Agent with model_id: {model_id}")
    model = get_model_from_config(model_id)
    
    supervisor = Agent(
        name="Supervisor",
        role="Coordinate and oversee the agent team, route queries, and synthesize results",
        description="Acts as the central coordinator for the multi-agent system, delegating tasks to specialist agents and ensuring quality answers",
        model=model,
        #     # max_tokens=500,
        #     # api_key=os.getenv("HF_TOKEN")
        # ),
        # model=Gemini(id="gemini-1.5-flash"),
        instructions=[
            "You are the supervisor coordinating a team of  agents: Web Search, Finance, Weather, Formula one SQL Database, and API agents.",
            "Use specialist agents for their expertise: Web Search for latest news, Finance for stock/earnings data, Weather for forecasts, SQL agent for structured F1 data, and API agent for cross-domain queries.",
            "Use Web search agent if specialist agents cannot answer the question or if the question requires up-to-date information.",
            "Analyze incoming queries and determine which agents are best suited to answer them.",
            "Delegate tasks to appropriate agents and wait for their responses before synthesizing.",
            "Always include sources and cite which agent provided each piece of information.",
            "Ensure the final response is well-organized, uses tables for data when appropriate, and addresses all parts of the user's query.",
            "If multiple agents are needed, coordinate their responses and identify connections/insights across domains.",
            "For ambiguous queries, ask clarifying questions or explain your routing decision to the user.",
        ],
        show_tool_calls=True,
        markdown=True,
    )
    logger.debug("Supervisor Agent initialized successfully")
    return supervisor


if __name__ == "__main__":
    # Test the supervisor agent
    supervisor_agent().print_response(
        "Who came third in 2010 in f1",
        stream=True
    )
