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
from agno.models.groq import Groq

from agno.tools.duckduckgo import DuckDuckGoTools

from dotenv import load_dotenv

load_dotenv(".env")

def web_agent():
    logger.debug("Initializing Web Agent")
    web_agent = Agent(
        name="Web Agent",
        role="Search the web for information",
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
        tools=[DuckDuckGoTools()],
        # instructions=["Always include sources"],
        show_tool_calls=True,
        markdown=True,
    )
    logger.debug("Web Agent initialized successfully")
    return web_agent

if __name__ == "__main__":
    logger.info("Running Web Agent standalone")
    web_agent().print_response("Tell me about sikkim", stream=True)
