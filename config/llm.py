"""LLM 工厂: 统一管理所有模型初始化, 换模型只改这里"""

from langchain_openai import ChatOpenAI
from config.settings import (
    DASHSCOPE_API_KEY,
    DASHSCOPE_BASE_URL,
    CODER_MODEL,
    REVIEWER_MODEL,
    SUMMARIZER_MODEL,
)


def get_coder_llm():
    """Coder: 千问云端, 生成能力强"""
    return ChatOpenAI(
        model=CODER_MODEL,
        api_key=DASHSCOPE_API_KEY,
        base_url=DASHSCOPE_BASE_URL,
        max_completion_tokens=2000,
    )


def get_reviewer_llm(structured_output=None):
    """Reviewer: 本地 Ollama, 速度快省钱"""
    llm = ChatOpenAI(
        model=REVIEWER_MODEL,
        api_key=DASHSCOPE_API_KEY,
        base_url=DASHSCOPE_BASE_URL,
        max_completion_tokens=2000,
    )
    if structured_output:
        return llm.with_structured_output(structured_output)
    return llm


def get_summarizer_llm():
    """Summarizer: 千问, 摘要要求不高"""
    return ChatOpenAI(
        model=SUMMARIZER_MODEL,
        api_key=DASHSCOPE_API_KEY,
        base_url=DASHSCOPE_BASE_URL,
    )


def get_supervisor_llm(structured_output=None):
    """Supervisor: 千问, 调度"""
    llm = ChatOpenAI(
        model=SUMMARIZER_MODEL,
        api_key=DASHSCOPE_API_KEY,
        base_url=DASHSCOPE_BASE_URL,
        max_completion_tokens=2000,
    )
    if structured_output:
        return llm.with_structured_output(structured_output)
    return llm
