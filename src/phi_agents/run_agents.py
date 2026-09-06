import os
import sys
import json
sys.path.append("src/")

from phi_agents.logger import get_logger
logger = get_logger(__name__)

from agno.team import Team
# from agno.playground import Playground, serve_playground_app

from phi_agents.functions.model_factory import get_model_from_config, get_default_model_id

from dotenv import load_dotenv
load_dotenv(".env")

logger.info("Loading environment and configuration...")

from phi_agents.functions.supervisor_agent import supervisor_agent
from phi_agents.functions.finance_agent import finance_agent
from phi_agents.functions.web_search import web_agent
from phi_agents.functions.weather_agent import weather_agent    
# from phi_agents.functions.browser_task_agent import browser_agent    
# from phi_agents.functions.sql_agent import get_sql_agent    
# from phi_agents.functions.api_calls import call_api_agent    
import streamlit as st

with open("config.json", "r") as file:
    config = json.load(file)

logger.info("Configuration loaded successfully")

# Get default model_id from configuration
default_model_id = get_default_model_id()
logger.info(f"Using model configuration: {default_model_id}")

# Set up parameters
db_host = config[os.getenv("ENV")]["db_host"]
db_port = config[os.getenv("ENV")]["db_port"]
db_name = config[os.getenv("ENV")]["db_name"]
db_user = config[os.getenv("ENV")]["db_user"]
db_password = config[os.getenv("ENV")]["db_password"]

logger.info("Initializing agent team...")
web_agent_instance = web_agent(model_id=default_model_id)
logger.info("Web agent initialized")
finance_agent_instance = finance_agent(model_id=default_model_id)
logger.info("Finance agent initialized")
weather_agent_instance = weather_agent(model_id=default_model_id)
logger.info("Weather agent initialized")
# browser_agent = browser_agent()
# sql_agent_instance = get_sql_agent(model_id=default_model_id)
# logger.info("SQL agent initialized")
# api_agent_instance = call_api_agent(model_id=default_model_id)
# logger.info("API agent initialized")
supervisor_instance = supervisor_agent(model_id=default_model_id)
logger.info("Supervisor agent initialized")

# Create team with dynamic model configuration
agent_team = Team(
    model=get_model_from_config(default_model_id),
    members=[supervisor_instance, finance_agent_instance, weather_agent_instance, web_agent_instance],
    # members=[supervisor_instance, finance_agent_instance, weather_agent_instance, api_agent_instance],
    instructions=["Always include sources", "Use tables to display data", "only use the agents in the team to answer questions", "Supervisor coordinates all agent interactions"],
    markdown=True,
)

logger.info("Agent team created successfully")

agent_team.print_response("What is the stock price of nvidia?", stream=True)
# agent_team.print_response("forecast of weather in cincinnati", stream=True)
# agent_team.print_response("current temperature in cincinnati as farenheit", stream=True)
# agent_team.print_response("what is yesterday's temperature  in london", stream=True)
# agent_team.print_response("tell me about sikkim", stream=True)
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


