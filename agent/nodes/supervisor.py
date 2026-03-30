from agent.core.base_agent import BaseAgent
from config.llm import get_supervisor_llm


class SupervisorAgent(BaseAgent):

    def run(self, state: dict) -> dict:
        llm = get_supervisor_llm()
