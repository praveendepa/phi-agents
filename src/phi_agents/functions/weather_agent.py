import os
import requests
import json
import sys
sys.path.append("src/")

from phi_agents.logger import get_logger
logger = get_logger(__name__)

from agno.agent import Agent
from phi_agents.functions.weather_tools import WeatherTools
from phi_agents.functions.model_factory import get_model_from_config, get_default_model_id

from dotenv import load_dotenv
load_dotenv(".env")

# def get_current_weather(location: str ="New York", unit:str ="celsius") -> str:
#     """Use this function to get current weather.

#     Args:
#         location (string): location to get weather data for.

#     Returns:
#         str: JSON string of location and temperature.
#     """
    
#     weather_api_key=os.environ.get("WEATHER_API_KEY")
#     api_url = "http://api.weatherapi.com/v1/current.json?key={}&q={}".format(weather_api_key,location)

#     response = requests.get(api_url)
#     return json.dumps({"location": location, "temperature": response.json()['current']['temp_c']})


def weather_agent(model_id: str = None):
    """Create a weather agent.
    
    Args:
        model_id: Model identifier in format 'provider:model_name'.
                 If None, uses default from config.json
    """
    if model_id is None:
        model_id = get_default_model_id()
    
    logger.debug(f"Initializing Weather Agent with model_id: {model_id}")
    model = get_model_from_config(model_id)
    
    weather_agent = Agent(
        name="Weather Agent",
        role="Get weather data",
        model=model,
        # tools=[get_current_weather],
        tools=[WeatherTools()],
        instructions=["Use tables to display data"],
        # show_tool_calls=True,
        markdown=True,
    )
    logger.debug("Weather Agent initialized successfully")
    return weather_agent

if __name__ == "__main__":
    logger.info("Running Weather Agent standalone")
    weather_agent().print_response("Get weather in singapore", stream=True)

# agent = Agent(name="Weather Agent", role="Get weather data", tools=[get_current_weather], show_tool_calls=True, markdown=True)
# agent.print_response("Get weather in singapore", stream=True)
