"""所有 Agent 的基类"""
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    @abstractmethod
    def run(self, state: dict) -> dict:
        """每个 Agent 必须实现 run 方法"""
        pass
