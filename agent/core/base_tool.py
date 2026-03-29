"""所有 Tool 的基类"""
from abc import ABC, abstractmethod


class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
