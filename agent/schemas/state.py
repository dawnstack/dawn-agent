"""Agent 状态和数据结构定义"""
from typing import List
from typing_extensions import TypedDict
from pydantic import BaseModel


class ReviewIssue(BaseModel):
    severity: str       # high / medium / low
    description: str    # 问题描述
    action: str         # 可执行的修改建议


class ReviewResult(BaseModel):
    passed: bool
    issues: List[ReviewIssue]


class AgentState(TypedDict):
    requirement: str        # 用户需求
    code: str               # 当前代码
    review: str             # 当前 review（JSON 字符串）
    iteration: int          # 循环计数
    review_history: list    # 历史 review 列表
    review_summary: str     # 压缩后的历史摘要
    preferences: dict       # 用户偏好（从 memory 加载）
    execution_result: dict  # 代码执行结果
