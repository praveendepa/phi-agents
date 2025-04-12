import os
import sys
sys.path.append("src/")

from agno.agent import Agent
from agno.playground import Playground, serve_playground_app

from agno.models.openai import OpenAIChat
from agno.models.huggingface import HuggingFace
# from agno.models.google import Gemini
# from agno.models.ollama import Ollama
# from agno.models.groq import Groq


from dotenv import load_dotenv

from phi_agents.functions.finance_agent import finance_agent
from phi_agents.functions.web_search import web_agent
from phi_agents.functions.weather_agent import weather_agent    
# from phi_agents.functions.browser_task_agent import browser_agent    
from phi_agents.functions.sql_agent import get_sql_agent    
from phi_agents.functions.api_calls import call_api_agent    

load_dotenv(".env")

web_agent = web_agent()
finance_agent = finance_agent()
weather_agent = weather_agent()
# browser_agent = browser_agent()
sql_agent = get_sql_agent()
api_agent = call_api_agent()

agent_team = Agent(
    model=OpenAIChat(id="gpt-4o"),
    # model=HuggingFace(
        # # id="meta-llama/Meta-Llama-3-8B-Instruct", 
        # id="meta-llama/Llama-3.2-3B-Instruct",
        # max_tokens=500,
        # api_key=os.getenv("HF_TOKEN")
    # ),
    # model=Gemini(id="gemini-1.5-flash"),
    # model=Ollama(id="myphi4"),
    # model=Groq(id="llama-3.3-70b-versatile"),
    team=[web_agent, finance_agent, weather_agent, api_agent],
    instructions=["Always include sources", "Use tables to display data", "only use the agents in the team to answer questions", "do not search the web"],
    show_tool_calls=True,
    markdown=True,
)

# agent_team.print_response("Summarize analyst recommendations and share the latest news for PG", stream=True)
# agent_team.print_response("forecast of weather in cincinnati", stream=True)
# agent_team.print_response("current temperature in cincinnati as farenheit", stream=True)
# agent_team.print_response("what is yesterday's temperature  in london", stream=True)
# agent_team.print_response("whats news in sikkim", stream=True)
# agent_team.print_response("Find a one-way flight from singapore to hyderabad on 28 January 2025 on Google Flights. Return me the cheapest option", stream=True)
agent_team.print_response("which formual 1 driver and team is the best combination?", stream=True)

# app = Playground(agents=[finance_agent, web_agent, weather_agent]).get_app()

# if __name__ == "__main__":
#     serve_playground_app("run_agents:app", reload=True)
