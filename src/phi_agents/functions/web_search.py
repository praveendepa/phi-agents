import os
import sys
sys.path.append("src/")

from phi_agents.logger import get_logger
logger = get_logger(__name__)

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from phi_agents.functions.model_factory import get_model_from_config, get_default_model_id

from dotenv import load_dotenv

load_dotenv(".env")

def web_agent(model_id: str = None):
    """Create a web search agent.
    
    Args:
        model_id: Model identifier in format 'provider:model_name'.
                 If None, uses default from config.json
    """
    if model_id is None:
        model_id = get_default_model_id()
    
    logger.debug(f"Initializing Web Agent with model_id: {model_id}")
    model = get_model_from_config(model_id)
    
    web_agent = Agent(
        name="Web Agent",
        role="Search the web for information",
        model=model,
        tools=[DuckDuckGoTools(enable_search=True, enable_news=True)],
        # instructions=["Always include sources"],
        # show_tool_calls=True,
        markdown=True,
    )
    logger.debug("Web Agent initialized successfully")
    return web_agent

if __name__ == "__main__":
    logger.info("Running Web Agent standalone")
    web_agent().print_response("Tell me about sikkim", stream=True)
