import os

from agno.agent import Agent

from agno.models.openai import OpenAIChat
from agno.models.huggingface import HuggingFace
from agno.models.google import Gemini
# from agno.models.ollama import Ollama
from agno.models.groq import Groq

from agno.tools.api import CustomApiTools

from dotenv import load_dotenv

load_dotenv(".env")

def call_api_agent():
    api_agent = Agent(
        name="API call Agent",
        role="API end point that takes a question about formula 1 drivers, teams, and race information",
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
        tools=[CustomApiTools(base_url="http://127.0.0.1:8000/my-sql-api?question=", make_request=True)],
        # instructions=["Always include sources"],
        show_tool_calls=True,
        markdown=True,
    )
    return api_agent

if __name__ == "__main__":
    call_api_agent().print_response("who is the best driver in 2010", stream=True)
