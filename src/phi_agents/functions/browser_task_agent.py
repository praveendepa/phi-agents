import os
import sys
sys.path.append("src/")

from phi_agents.logger import get_logger
logger = get_logger(__name__)

from agno.agent import Agent

from agno.models.openai import OpenAIChat
from agno.models.huggingface import HuggingFace
from agno.models.google import Gemini
# from agno.models.ollama import Ollama

from phi_agents.functions.browser_tools import BrowserTools

from dotenv import load_dotenv

load_dotenv(".env")

def browser_agent():
    logger.debug("Initializing Browser Agent")
    browser_agent = Agent(
        name="Browser Search Agent",
        role="Use the browser to do a series of tasks to answer a user query",
        # model=OpenAIChat(id="gpt-4o"),
        # model=HuggingFaceChat(
        #     id="meta-llama/Meta-Llama-3-8B-Instruct", 
        #     #id="meta-llama/Llama-3.2-3B-Instruct",
        #     #max_tokens=500,
        #     # api_key=os.getenv("HF_TOKEN")
        # ),
        # model=Gemini(id="gemini-1.5-flash"),
        # model=Ollama(id="myphi4"),
        tools=[BrowserTools()],
        instructions=["Call the functions using aynchronous calls"],
        show_tool_calls=True,
        markdown=True,
    )
    logger.debug("Browser Agent initialized successfully")
    return browser_agent

if __name__ == "__main__":
    logger.info("Running Browser Agent standalone")
    browser_agent().print_response("Find a one-way flight from singapore to hyderabad on 28 January 2025.", stream=True)