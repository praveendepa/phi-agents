import sys
sys.path.append("src/")

from phi_agents.logger import get_logger
logger = get_logger(__name__)

from agno.agent import Agent

from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
# from agno.models.ollama import Ollama

from agno.tools.yfinance import YFinanceTools

from dotenv import load_dotenv
load_dotenv(".env")

def finance_agent():
    logger.debug("Initializing Finance Agent")
    finance_agent = Agent(
        name="Finance Agent",
        role="Get financial data",
        model=OpenAIChat(id="gpt-4o"),
        # model=Gemini(id="gemini-1.5-flash"),
        # model=Ollama(id="myphi4"),
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
        instructions=["Use tables to display data"],
        show_tool_calls=True,
        markdown=True,
    )
    logger.debug("Finance Agent initialized successfully")
    return finance_agent

if __name__ == "__main__":
    logger.info("Running Finance Agent standalone")
    finance_agent().print_response("Summarize analyst recommendations for NVDA", stream=True)
