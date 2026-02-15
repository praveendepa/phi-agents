"""Model Factory - Utility for instantiating models based on configuration."""

import json
import os
import sys
sys.path.append("src/")

from phi_agents.logger import get_logger
logger = get_logger(__name__)

from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
from agno.models.anthropic import Claude
from agno.models.huggingface import HuggingFace
from agno.models.groq import Groq


def get_model_from_config(model_id: str = None):
    """
    Instantiate a model based on the model_id.
    
    Args:
        model_id: Model identifier in format 'provider:model_name'
                 If None, uses default from config.json
    
    Returns:
        Instantiated model object
        
    Raises:
        ValueError: If provider is unsupported or model_id format is invalid
    """
    
    # Load config if model_id not provided
    if model_id is None:
        with open("config.json", "r") as file:
            config = json.load(file)
        
        default_provider = config["models"]["default_provider"]
        model_name = config["models"]["providers"][default_provider]["model_name"]
        model_id = f"{default_provider}:{model_name}"
        logger.debug(f"Using default model configuration: {model_id}")
    
    # Parse model_id
    try:
        provider, model_name = model_id.split(":")
    except ValueError:
        logger.error(f"Invalid model_id format: {model_id}. Expected 'provider:model_name'")
        raise ValueError(f"Invalid model_id format: {model_id}. Expected 'provider:model_name'")
    
    logger.debug(f"Instantiating {provider} model: {model_name}")
    
    # Select appropriate model class based on provider
    if provider == "openai":
        return OpenAIChat(id=model_name)
    elif provider == "google":
        return Gemini(id=model_name)
    elif provider == "anthropic":
        return Claude(id=model_name)
    elif provider == "huggingface":
        return HuggingFace(
            id=model_name,
            api_key=os.getenv("HF_TOKEN")
        )
    elif provider == "groq":
        return Groq(id=model_name)
    else:
        logger.error(f"Unsupported model provider: {provider}")
        raise ValueError(f"Unsupported model provider: {provider}")


def get_default_model_id():
    """
    Get the default model_id from config.json.
    
    Returns:
        Model identifier in format 'provider:model_name'
    """
    with open("config.json", "r") as file:
        config = json.load(file)
    
    default_provider = config["models"]["default_provider"]
    model_name = config["models"]["providers"][default_provider]["model_name"]
    return f"{default_provider}:{model_name}"
