import os

from phi.agent import Agent

from phi.model.openai import OpenAIChat
from phi.model.huggingface import HuggingFaceChat
from phi.model.google import Gemini
from phi.model.ollama import Ollama
from phi.model.groq import Groq

from phi.tools.duckduckgo import DuckDuckGo

from dotenv import load_dotenv

load_dotenv(".env")

def web_agent():
    web_agent = Agent(
        name="Web Agent",
        role="Search the web for information",
        # model=OpenAIChat(id="gpt-4o"),
        # model=HuggingFaceChat(
        #     id="meta-llama/Meta-Llama-3-8B-Instruct", 
        #     #id="meta-llama/Llama-3.2-3B-Instruct",
        #     #max_tokens=500,
        #     # api_key=os.getenv("HF_TOKEN")
        # ),
        # model=Gemini(id="gemini-1.5-flash"),
        # model=Ollama(id="myphi4"),
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[DuckDuckGo()],
        # instructions=["Always include sources"],
        show_tool_calls=True,
        markdown=True,
    )
    return web_agent

if __name__ == "__main__":
    web_agent().print_response("Tell me about sikkim", stream=True)
