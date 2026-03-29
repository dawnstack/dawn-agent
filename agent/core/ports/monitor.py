"""监控接口：定义契约"""
from abc import ABC, abstractmethod


class IMonitor(ABC):
    @abstractmethod
    def log(self, event: str, data: dict): pass

    @abstractmethod
    def trace(self, span_name: str, data: dict): pass

    @abstractmethod
    def metric(self, name: str, value: float, tags: dict = {}): pass
