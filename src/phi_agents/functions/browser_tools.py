import requests
from os import getenv
from typing import Optional, Dict, Any, List
import json

from agno.tools import Toolkit
from agno.utils.log import logger

from langchain_openai import ChatOpenAI
from browser_use import Agent as BrowserAgent
from browser_use import Controller
from browser_use.browser.browser import Browser, BrowserConfig
import asyncio

from dotenv import load_dotenv
load_dotenv(".env")

import time

class BrowserTools(Toolkit):
    def __init__(
        self,
        api_key: Optional[str] = None):
    
        super().__init__(name="browser_tools")

        self.browser = Browser(
            config=BrowserConfig(
                headless=True,
            )
        )
        self.controller = Controller()

        self.register(self.get_result)

        
    def get_result(self, query: str = "Find one-way flight from Singapore to Hyderabad on 28 January 2025 on Google Flights") -> str:
        """Use this function to run a set of tasks on the browser.

        Args:
            query (string): question from the user.

        Returns:
            str: JSON string of query and the result.
        """

        print(query)
        agent = BrowserAgent(
            task=query,
            llm=ChatOpenAI(model="gpt-4o"),
            controller=self.controller,
            browser=self.browser,
            )
        
        # result = await agent.run()
        result = agent.run()
        time.sleep(20)
        # await self.browser.close()
        self.browser.close()
        print(result)
        return result
    
if __name__ == "__main__":
    browser_tools = BrowserTools()
    asyncio.run(browser_tools.get_result())

