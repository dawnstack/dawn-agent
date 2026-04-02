"""Summarizer Agent: 压缩历史 review, 防止 token 爆炸"""

from agent.core.base_agent import BaseAgent
from config.llm import get_summarizer_llm


class SummarizerAgent(BaseAgent):

    def run(self, state: dict) -> dict:
        if len(state.get("review_history", [])) < 3:
            return {}
        print("\n压缩历史 review...")
        llm = get_summarizer_llm()
        history_text = "\n".join(
            [f"第{i+1}轮: {r['issues']}" for i, r in enumerate(state["review_history"])]
        )
        response = llm.invoke(
            f"总结以下多轮review的主要问题和改进趋势(3-5句话)。"
            f"如果同一个问题在多轮中出现，请明确使用'反复出现'或'持续存在'来描述。\n{history_text}"
        )
        print(f"摘要: {response.content}")
        return {"review_summary": response.content}
