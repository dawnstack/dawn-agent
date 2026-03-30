"""存储接口: 定义契约, plugins 必须实现"""
from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def get(self, key: str): pass

    @abstractmethod
    def set(self, key: str, value): pass

    @abstractmethod
    def delete(self, key: str): pass

    @abstractmethod
    def list_keys(self, prefix: str = "") -> list: pass
