import json
from agent.tools.output_cleaner import clean_json
from agent.core.base_agent import BaseAgent
from config.llm import get_supervisor_llm


class SupervisorAgent(BaseAgent):

    def run(self, state: dict) -> dict:
        llm = get_supervisor_llm()

        review = state.get("review", "{}")
        review_data = json.loads(review) if review else {}
        iteration = state.get("iteration", 0)
        review_summary = state.get("review_summary", "暂无历史摘要")
        code = state.get("code", "暂无代码")
        requirement = state.get("requirement", "")

        prompt = f"""
你是一个代码生成流程的总调度员（Supervisor）。
你的职责是根据当前状态，决定下一步行动。

## 当前状态
- 用户需求：{requirement}
- 当前迭代次数：{iteration}
- 历史摘要：{review_summary}
- 当前代码：
{code}

## 最新 Review 结果
{json.dumps(review_data, ensure_ascii=False, indent=2) if review_data else "尚未进行 Review（首次运行）"}

## 你的决策规则
1. 如果是首次运行（无 review），应该让 coder 开始生成代码
2. 如果 review 通过（passed: true），任务完成，结束流程
3. 如果问题严重（high severity 问题超过 2 个）且迭代已超过 5 次，结束流程避免无限循环
4. 如果迭代次数超过 8 次，无论如何结束流程
5. 如果历史摘要中出现"反复出现"、"持续存在"、"多轮"等字样，说明 coder 无法自行解决该问题，
   应立即结束流程，在 reason 中说明是哪个问题导致终止，不要继续循环浪费资源
   (少于 4 次不触发此规则，给 coder 足够机会)
6. 其他情况，继续让 coder 修改代码

## 输出格式
请严格返回 JSON，不要有任何其他文字：
{{
    "decision": "coder" 或 "end",
    "reason": "你的决策理由",
    "priority_issues": ["最重要的问题1", "最重要的问题2"]
}}
        """

        response = llm.invoke(prompt)
        result = json.loads(clean_json(response.content))

        decision = result.get("decision", "coder").strip().lower()
        if decision not in ("coder", "end"):
            print(f"[Supervisor] 非法决策值 '{decision}'，默认继续 coder")
            decision = "coder"

        print(f"\n[Supervisor] 决策：{decision}")
        print(f"[Supervisor] 理由：{result.get('reason', '')}")
        if result.get("priority_issues"):
            print(f"[Supervisor] 优先处理：{result['priority_issues']}")

        return {
            "next": decision,
            "supervisor_instructions": json.dumps(result, ensure_ascii=False),
        }
