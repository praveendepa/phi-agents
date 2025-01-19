import requests
from os import getenv
from typing import Optional, Dict, Any, List
import json

from phi.tools import Toolkit
from phi.utils.log import logger


class WeatherTools(Toolkit):
    def __init__(
        self,
        api_key: Optional[str] = None):

        super().__init__(name="weather_tools")

        self.api_key = api_key or getenv("WEATHER_API_KEY")
        if not self.api_key:
            logger.error("WEATHER_API_KEY not set. Please set the WEATHER_API_KEY environment variable.")

        self.base_url = "http://api.weatherapi.com/v1/"

        self.register(self.get_current_weather)
        self.register(self.get_forecast)
        self.register(self.get_weather_history)
        
    def get_current_weather(self, location: str = "New York", unit:str ="celsius") -> str:
        """Use this function to get current weather.

        Args:
            location (string): location to get weather data for.

        Returns:
            str: JSON string of location, temperature and units of temperature (celsius or farenheit).
        """
        endpoint = f"{self.base_url}current.json"
        params = {
            'key': self.api_key,
            'q': location
        }
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            # return json.dumps({"location": location, "temperature": response.json()['current']['temp_c']})
            data = response.json()
            return json.dumps({
                "location": location,
                "temperature": data['current']['temp_c'] if unit == "celsius" else data['current']['temp_f'],
                "unit": unit,
            })
        else:
            response.raise_for_status()

    def get_forecast(self, location: str = "New York", days: int = 3) -> str:
        """Use this function to get weather forecast.

        Args:
            location (string): location to get weather forecast for.
            days (int): number of days to get forecast for.

        Returns:
            str: JSON string of forecast data.
        """
        endpoint = f"{self.base_url}forecast.json"
        params = {
            'key': self.api_key,
            'q': location,
            'days': days
        }
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_weather_history(self, location: str, date: str) -> str:
        """Use this function to get historical weather data.

        Args:
            location (string): location to get historical weather data for.
            date (string): date to get historical weather data for in YYYY-MM-DD format.

        Returns:
            str: JSON string of historical weather data.
        """
        endpoint = f"{self.base_url}history.json"
        params = {
            'key': self.api_key,
            'q': location,
            'dt': date
        }
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()