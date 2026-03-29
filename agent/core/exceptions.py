"""统一异常定义"""

class AgentException(Exception):
    pass

class ToolException(Exception):
    pass

class LLMException(Exception):
    pass

class StorageException(Exception):
    pass
