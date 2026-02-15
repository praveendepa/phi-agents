import os
import sys
import json
sys.path.append("src/")

from phi_agents.logger import get_logger
logger = get_logger(__name__)

from agno.agent import Agent
from agno.playground import Playground, serve_playground_app

from agno.models.openai import OpenAIChat
from agno.models.huggingface import HuggingFace
# from agno.models.google import Gemini
# from agno.models.ollama import Ollama
# from agno.models.groq import Groq


from dotenv import load_dotenv
load_dotenv(".env")

logger.info("Loading environment and configuration...")

from phi_agents.functions.supervisor_agent import supervisor_agent
from phi_agents.functions.finance_agent import finance_agent
from phi_agents.functions.web_search import web_agent
from phi_agents.functions.weather_agent import weather_agent    
# from phi_agents.functions.browser_task_agent import browser_agent    
from phi_agents.functions.sql_agent import get_sql_agent    
from phi_agents.functions.api_calls import call_api_agent    
import streamlit as st

with open("config.json", "r") as file:
    config = json.load(file)

logger.info("Configuration loaded successfully")

# Set up parameters
db_host = config[os.getenv("ENV")]["db_host"]
db_port = config[os.getenv("ENV")]["db_port"]
db_name = config[os.getenv("ENV")]["db_name"]
db_user = config[os.getenv("ENV")]["db_user"]
db_password = config[os.getenv("ENV")]["db_password"]

logger.info("Initializing agent team...")
web_agent = web_agent()
logger.info("Web agent initialized")
finance_agent = finance_agent()
logger.info("Finance agent initialized")
weather_agent = weather_agent()
logger.info("Weather agent initialized")
# browser_agent = browser_agent()
sql_agent = get_sql_agent()
logger.info("SQL agent initialized")
api_agent = call_api_agent()
logger.info("API agent initialized")
supervisor = supervisor_agent()
logger.info("Supervisor agent initialized")

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
    team=[supervisor, finance_agent, weather_agent, api_agent],
    instructions=["Always include sources", "Use tables to display data", "only use the agents in the team to answer questions", "Supervisor coordinates all agent interactions"],
    show_tool_calls=True,
    markdown=True,
)

logger.info("Agent team created successfully")

# agent_team.print_response("Summarize analyst recommendations and share the latest news for PG", stream=True)
# agent_team.print_response("forecast of weather in cincinnati", stream=True)
# agent_team.print_response("current temperature in cincinnati as farenheit", stream=True)
# agent_team.print_response("what is yesterday's temperature  in london", stream=True)
# agent_team.print_response("whats news in sikkim", stream=True)
# agent_team.print_response("Find a one-way flight from singapore to hyderabad on 28 January 2025 on Google Flights. Return me the cheapest option", stream=True)
# agent_team.print_response("which formual 1 driver and team is the best combination?", stream=True)
# agent_team.print_response("which team won most formuala 1 races in 2012?", stream=True)



# Streamlit app
st.set_page_config(page_title="Agent Team Frontend", layout="wide")

st.title("Agent Team Frontend")
st.markdown("Ask questions and get intelligent responses from the agent team.")

# Input field for user question
question = st.text_input("Enter your question:", "")

# Button to trigger the agent response
if st.button("Get Response"):
    if question.strip():
        logger.info(f"User question received: {question[:50]}...")
        with st.spinner("🤔 Thinking..."):
            try:
                response = ""
                run_response = agent_team.run(question, stream=True)
                for chunk in run_response:
                    if chunk.content:
                        response += chunk.content
                # Display the full response after it is completely collected
                st.markdown(response)
                logger.info(f"Response generated successfully for question: {question[:50]}...")
            except Exception as e:
                logger.error(f"Error processing question: {str(e)}", exc_info=True)
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a question to proceed.")


# app = Playground(agents=[finance_agent, web_agent, weather_agent]).get_app()

# if __name__ == "__main__":
#     serve_playground_app("run_agents:app", reload=True)


