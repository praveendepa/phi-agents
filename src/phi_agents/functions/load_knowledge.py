import sys
sys.path.append("src/")

from agents import agent_knowledge
from phi_agents.logger import get_logger
logger = get_logger(__name__)


def load_knowledge(recreate: bool = True):
    logger.info(f"Loading SQL agent knowledge with recreate={recreate}")
    agent_knowledge.load(recreate=recreate)
    logger.info("SQL agent knowledge loaded successfully")


if __name__ == "__main__":
    load_knowledge()
