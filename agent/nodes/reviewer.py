"""Reviewer Agent: 负责代码审查"""

from agent.core.base_agent import BaseAgent
from config.llm import get_reviewer_llm
from agent.schemas.state import ReviewResult
from agent.tools.retry import with_retry


class ReviewerAgent(BaseAgent):

    @with_retry(max_retries=3, delay=1.0)
    def run(self, state: dict) -> dict:
        print(f"\nReviewer 第 {state['iteration']} 次 review...")
        llm = get_reviewer_llm(structured_output=ReviewResult)

        exec_result = state.get("execution_result", {})
        exec_info = (
            f"执行成功: {exec_result.get('stdout', '')}"
            if exec_result.get("success")
            else f"执行失败: {exec_result.get('stderr', '')}"
        )

        prompt = f"""you are a python3 code reviewer.
review the below code and execution result.

codes: {state['code']}
execution result: {exec_info}

## Severity Definition (STRICT)
- high: causes crashes, data loss, security vulnerabilities, or incorrect results. MUST fix.
- medium: bad practices, missing error handling, performance issues. SHOULD fix.
- low: style, naming, minor readability. NICE to fix.

## Passing Rules
- passed=true if: no high severity issues found
- passed=true if: execution succeeded and only medium/low issues exist  
- passed=false ONLY if: there are one or more high severity issues

## Review Checklist
1. Does it crash or produce wrong results? (high)
2. Does it handle exceptions where needed? (medium)
3. Is it reasonably readable? (low)

return JSON only:
{{
  "passed": true or false,
  "issues": [{{"severity": "high/medium/low", "description": "...", "action": "..."}}]
}}"""

        response: ReviewResult = llm.invoke(prompt)
        print(f"\n=== REVIEWER OUTPUT ===\n{response}\n=== END ===\n")

        history = state.get("review_history", [])
        history.append(response.model_dump())
        return {"review": response.model_dump_json(), "review_history": history}
