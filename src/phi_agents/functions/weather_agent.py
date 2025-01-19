import os
import requests
import json
import sys
sys.path.append("src/")

from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.model.google import Gemini
from phi.model.ollama import Ollama

from phi_agents.functions.weather_tools import WeatherTools

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


def weather_agent():
    weather_agent = Agent(
        name="Weather Agent",
        role="Get weather data",
        # model=OpenAIChat(id="gpt-4o"),
        # model=Gemini(id="gemini-1.5-flash"),
        # model=Ollama(id="myphi4"),
        # tools=[get_current_weather],
        tools=[WeatherTools()],
        instructions=["Use tables to display data"],
        show_tool_calls=True,
        markdown=True,
    )
    return weather_agent

if __name__ == "__main__":
    weather_agent().print_response("Get weather in singapore", stream=True)

# agent = Agent(name="Weather Agent", role="Get weather data", tools=[get_current_weather], show_tool_calls=True, markdown=True)
# agent.print_response("Get weather in singapore", stream=True)
