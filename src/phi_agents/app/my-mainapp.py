
import os
import sys
sys.path.append("src/")
# uvicorn src.phi_agents.app.my-mainapp:app  --env-file .env --reload

from phi_agents.logger import get_logger
logger = get_logger(__name__)

# from fastapi import FastAPI
# app = FastAPI()

# @app.get("/my-first-api")
# def hello(name: str):
#   return {'Hello there, this is ' + name + '!'} 


from dotenv import load_dotenv
load_dotenv("./.env") 

from fastapi import FastAPI, HTTPException
from phi_agents.functions.sql_agent import get_sql_agent

logger.info("FastAPI application initialized")
app = FastAPI()

@app.get("/my-sql-api")
def sql_agent_endpoint(question: str = "champion driver in 2010", model_id: str = "openai:gpt-4o", session_id: str = None, debug_mode: bool = True):
    logger.info(f"SQL API endpoint called - Question: {question[:50]}..., Model: {model_id}")
    
    # # initialize parameters
    # project_id = os.getenv("project_id")
    # region = os.getenv("region")
    # instance_name = os.getenv("instance_name")
    # db_user = os.getenv("db_user")
    # db_password = os.getenv("db_password")
    # db_host = os.getenv("db_host")
    # db_port = os.getenv("db_port")
    # db_name = os.getenv("db_name")
    try:
        logger.debug(f"Creating SQL agent with model_id: {model_id}")
        sql_agent = get_sql_agent(model_id=model_id)
        response_stream = sql_agent.run(question, stream=True)
        response = ""
        for _resp_chunk in response_stream:
            # Display response
            if _resp_chunk.content is not None:
                response += _resp_chunk.content
        logger.info(f"SQL API endpoint response generated successfully")
        return response
        # return add_message("assistant", response, sql_agent.run_response.tools)
    except Exception as e:
        logger.error(f"Error in SQL API endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))