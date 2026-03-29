"""全局配置"""
import os

# LLM
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
CODER_MODEL = "qwen-coder-turbo-0919"
REVIEWER_MODEL = "qwen3:8b"

# Agent
MAX_ITERATIONS = 3
CODE_EXECUTION_TIMEOUT = 5

# Storage
DB_PATH = "memory.db"
