"""Coder Agent：负责生成和修改代码"""

import json
from agent.core.base_agent import BaseAgent
from config.llm import get_coder_llm
from agent.tools.retry import with_retry


class CoderAgent(BaseAgent):

    @with_retry(max_retries=3, delay=1.0)
    def run(self, state: dict) -> dict:
        print(f"\n🤖 Coder 第 {state['iteration'] + 1} 次写代码...")
        llm = get_coder_llm()
        prompt = (
            self._build_fix_prompt(state)
            if (state["code"] and state["review"])
            else self._build_generate_prompt(state)
        )
        prompt = self._inject_preferences(prompt, state)
        response = llm.invoke(prompt)
        return {"code": response.content, "iteration": state["iteration"] + 1}

    def _build_generate_prompt(self, state: dict) -> str:
        return f"""you are a python3 specialist.
please write codes based on the below requirements.
only return codes, no explanation, no markdown code blocks.
requirements: {state['requirement']}"""

    def _build_fix_prompt(self, state: dict) -> str:
        review = json.loads(state["review"])
        issues_text = "\n".join(
            [
                f"- [{i['severity']}] {i['description']}\n  修改方式：{i['action']}"
                for i in review["issues"]
            ]
        )
        return f"""you are a python3 specialist.
your last version: {state['code']}
review suggestions:
{issues_text}
please modify based on suggestions, do not rewrite.
only return codes, no explanation, no markdown code blocks."""

    def _inject_preferences(self, prompt: str, state: dict) -> str:
        prefs = state.get("preferences", {})
        hints = ""
        if prefs.get("code_style", {}).get("type_hints"):
            hints += "- 必须加类型注解\n"
        if prefs.get("code_style", {}).get("docstring"):
            hints += "- 必须加 docstring\n"
        if prefs.get("preferred_libraries"):
            hints += f"- 优先使用: {', '.join(prefs['preferred_libraries'])}\n"
        return prompt + (f"\n用户偏好:\n{hints}" if hints else "")
