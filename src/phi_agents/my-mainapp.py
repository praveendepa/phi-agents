
import os
import sys
sys.path.append("src/")
# uvicorn src.phi_agents.my-mainapp:app  --reload

# from fastapi import FastAPI
# app = FastAPI()

# @app.get("/my-first-api")
# def hello(name: str):
#   return {'Hello there, this is ' + name + '!'} 

from fastapi import FastAPI, HTTPException
from phi_agents.functions.sql_agent import get_sql_agent

app = FastAPI()

@app.get("/my-sql-api")
def sql_agent_endpoint(question: str = "champion driver in 2010", model_id: str = "openai:gpt-4o", session_id: str = None, debug_mode: bool = True):
    try:
        sql_agent = get_sql_agent(model_id=model_id)
        response_stream = sql_agent.run(question, stream=True)
        response = ""
        for _resp_chunk in response_stream:
            # Display response
            if _resp_chunk.content is not None:
                response += _resp_chunk.content
        return response
        # return add_message("assistant", response, sql_agent.run_response.tools)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))