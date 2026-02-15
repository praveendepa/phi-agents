import os
import json
import sys
sys.path.append("src/")

from phi_agents.logger import get_logger
logger = get_logger(__name__)

from agno.agent import Agent

from agno.models.openai import OpenAIChat
from agno.models.huggingface import HuggingFace
from agno.models.google import Gemini
# from agno.models.ollama import Ollama
from agno.models.groq import Groq

from agno.tools.api import CustomApiTools

from dotenv import load_dotenv
load_dotenv(".env")

with open("config.json", "r") as file:
    config = json.load(file)

# Set up parameters
db_host = config[os.getenv("ENV")]["db_host"]

def call_api_agent():
    logger.debug("Initializing API Call Agent")
    api_agent = Agent(
        name="API call Agent",
        role="API end point that takes a question about formula 1 drivers, teams, and race information",
        model=OpenAIChat(id="gpt-4o"),
        # model=HuggingFaceChat(
        #     id="meta-llama/Meta-Llama-3-8B-Instruct", 
        #     # id="meta-llama/Llama-3.2-3B-Instruct",
        #     # max_tokens=500,
        #     # api_key=os.getenv("HF_TOKEN")
        # ),
        # model=Gemini(id="gemini-1.5-flash"),
        # model=Ollama(id="myphi4"),
        # model=Groq(id="llama-3.3-70b-versatile"),
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
