import sys
sys.path.append("src/")

from phi_agents.logger import get_logger
logger = get_logger(__name__)

from agno.agent import Agent
from agno.tools.finance import FinanceTools
from agno.tools.finance.providers import YFinance

from phi_agents.functions.model_factory import get_model_from_config, get_default_model_id

from dotenv import load_dotenv
load_dotenv(".env")

def finance_agent(model_id: str = None):
    """Create a finance agent.
    
    Args:
        model_id: Model identifier in format 'provider:model_name'.
                 If None, uses default from config.json
    """
    if model_id is None:
        model_id = get_default_model_id()
    
    logger.debug(f"Initializing Finance Agent with model_id: {model_id}")
    model = get_model_from_config(model_id)
    
    finance_agent = Agent(
        name="Finance Agent",
        role="Get financial data",
        model=model,
        tools=[FinanceTools(provider=YFinance())],
        instructions=["Use tables to display data"],
        # show_tool_calls=True,
        markdown=True,
    )
    logger.debug("Finance Agent initialized successfully")
    return finance_agent

if __name__ == "__main__":
    logger.info("Running Finance Agent standalone")
    finance_agent().print_response("Summarize analyst recommendations for NVDA", stream=True)
