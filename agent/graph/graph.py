"""Graph 定义: 节点连接和流程控制"""
import json
from langgraph.graph import StateGraph, START, END
from agent.schemas.state import AgentState
from agent.nodes.coder import CoderAgent
from agent.nodes.reviewer import ReviewerAgent
from agent.nodes.summarizer import SummarizerAgent
from agent.tools.code_executor import CodeExecutor
from config.settings import MAX_ITERATIONS

# 实例化
coder = CoderAgent()
reviewer = ReviewerAgent()
summarizer = SummarizerAgent()
executor = CodeExecutor()


def executor_node(state: AgentState) -> dict:
    print("\n执行代码...")
    result = executor.execute(state["code"])
    print(f"{'执行成功' if result['success'] else '执行失败: ' + result['stderr'][:100]}")
    return {"execution_result": result}


def should_continue(state: AgentState) -> str:
    if state["iteration"] >= MAX_ITERATIONS:
        print("达到最大循环次数, 强制结束")
        return END
    review = json.loads(state["review"])
    if review["passed"]:
        print("Review 通过!")
        return END
    print(f"发现 {len(review['issues'])} 个问题, 继续修改...")
    for i in review["issues"]:
        print(f"  {i['action']}")
    return "coder"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("coder", coder.run)
    graph.add_node("executor", executor_node)
    graph.add_node("reviewer", reviewer.run)
    graph.add_node("summarize", summarizer.run)

    graph.add_edge(START, "coder")
    graph.add_edge("coder", "executor")
    graph.add_edge("executor", "reviewer")
    graph.add_edge("reviewer", "summarize")
    graph.add_conditional_edges("summarize", should_continue)

    return graph.compile()
