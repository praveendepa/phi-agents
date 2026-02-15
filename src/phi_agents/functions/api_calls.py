import os
import json
import sys
sys.path.append("src/")

from phi_agents.logger import get_logger
logger = get_logger(__name__)

from agno.agent import Agent
from agno.tools.api import CustomApiTools

from phi_agents.functions.model_factory import get_model_from_config, get_default_model_id

from dotenv import load_dotenv
load_dotenv(".env")

with open("config.json", "r") as file:
    config = json.load(file)

# Set up parameters
db_host = config[os.getenv("ENV")]["db_host"]

def call_api_agent(model_id: str = None):
    """Create an API call agent.
    
    Args:
        model_id: Model identifier in format 'provider:model_name'.
                 If None, uses default from config.json
    """
    if model_id is None:
        model_id = get_default_model_id()
    
    logger.debug(f"Initializing API Call Agent with model_id: {model_id}")
    model = get_model_from_config(model_id)
    
    api_agent = Agent(
        name="API call Agent",
        role="API end point that takes a question about formula 1 drivers, teams, and race information",
        model=model,
        # tools=[CustomApiTools(base_url="http://127.0.0.1:8000/my-sql-api?question=", make_request=True)],
        # tools=[CustomApiTools(base_url=f"http://{db_host}:8000/my-sql-api?question=", make_request=True)],
        tools=[CustomApiTools(base_url="https://sample-239471998272.us-central1.run.app/my-sql-api?question=", make_request=True)],
        # instructions=["Always include sources"],
        show_tool_calls=True,
        markdown=True,
    )
    logger.debug("API Call Agent initialized successfully")
    return api_agent

if __name__ == "__main__":
    logger.info("Running API Call Agent standalone")
    call_api_agent().print_response("who is the best driver in 2010", stream=True)
