"""Session 接口: 定义契约"""
from abc import ABC, abstractmethod


class ISession(ABC):
    @abstractmethod
    def create(self, session_id: str) -> dict: pass

    @abstractmethod
    def get(self, session_id: str) -> dict: pass

    @abstractmethod
    def update(self, session_id: str, state: dict): pass

    @abstractmethod
    def delete(self, session_id: str): pass
