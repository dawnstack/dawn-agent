"""Reviewer Agent：负责代码审查"""

from agent.core.base_agent import BaseAgent
from config.llm import get_reviewer_llm
from agent.schemas.state import ReviewResult
from agent.tools.retry import with_retry


class ReviewerAgent(BaseAgent):

    @with_retry(max_retries=3, delay=1.0)
    def run(self, state: dict) -> dict:
        print(f"\n🔍 Reviewer 第 {state['iteration']} 次 review...")
        llm = get_reviewer_llm(structured_output=ReviewResult)

        exec_result = state.get("execution_result", {})
        exec_info = (
            f"执行成功：{exec_result.get('stdout', '')}"
            if exec_result.get("success")
            else f"执行失败：{exec_result.get('stderr', '')}"
        )

        prompt = f"""you are a strict python3 reviewer.
review the below code:
1. potential bugs  2. error handling  3. readability  4. best practices

codes: {state['code']}
execution result: {exec_info}

Judgment: passed=false only for high severity, otherwise passed=true.

请严格按照以下 json 格式返回：
{{
  "passed": true,
  "issues": [{{"severity": "high/medium/low", "description": "问题描述", "action": "修改建议"}}]
}}"""

        response: ReviewResult = llm.invoke(prompt)
        print(f"\n=== REVIEWER OUTPUT ===\n{response}\n=== END ===\n")

        history = state.get("review_history", [])
        history.append(response.model_dump())
        return {"review": response.model_dump_json(), "review_history": history}
