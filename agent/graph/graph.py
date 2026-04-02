"""Graph 定义: 节点连接和流程控制"""

from langgraph.graph import StateGraph, START, END
from agent.schemas.state import AgentState
from agent.nodes.coder import CoderAgent
from agent.nodes.reviewer import ReviewerAgent
from agent.nodes.summarizer import SummarizerAgent
from agent.nodes.supervisor import SupervisorAgent
from agent.tools.code_executor import CodeExecutor
from config.settings import MAX_ITERATIONS

# 实例化
coder = CoderAgent()
reviewer = ReviewerAgent()
summarizer = SummarizerAgent()
executor = CodeExecutor()
supervisor = SupervisorAgent()


def executor_node(state: AgentState) -> dict:
    print("\n执行代码...")
    result = executor.execute(state["code"])
    print(
        f"{'执行成功' if result['success'] else '执行失败: ' + result['stderr'][:100]}"
    )
    return {"execution_result": result}

def route_supervisor(state: AgentState) -> str:
    if state.get("iteration", 0) >= MAX_ITERATIONS:
        print(f"[Safety] 达到绝对上限 {MAX_ITERATIONS} 次, 强制结束")
        return "end"
    return state.get("next", "coder")


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor.run)
    graph.add_node("coder", coder.run)
    graph.add_node("executor", executor_node)
    graph.add_node("reviewer", reviewer.run)
    graph.add_node("summarize", summarizer.run)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "coder": "coder",
            "end": END,
        },
    )

    graph.add_edge("coder", "executor")
    graph.add_edge("executor", "reviewer")
    graph.add_edge("reviewer", "summarize")
    graph.add_edge("summarize", "supervisor")

    return graph.compile()
