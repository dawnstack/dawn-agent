"""代码执行工具"""
import subprocess
from agent.core.base_tool import BaseTool
from config.settings import CODE_EXECUTION_TIMEOUT


class CodeExecutor(BaseTool):
    name = "code_executor"
    description = "在沙盒环境中执行 Python 代码"

    def execute(self, code: str) -> dict:
        code = self._clean_code(code)
        try:
            result = subprocess.run(
                ["python3", "-c", code],
                capture_output=True,
                text=True,
                timeout=CODE_EXECUTION_TIMEOUT,
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {"stdout": "", "stderr": f"执行超时（超过{CODE_EXECUTION_TIMEOUT}秒）", "success": False}

    def _clean_code(self, code: str) -> str:
        code = code.strip()
        if code.startswith("```"):
            code = code.split("```")[1]
            if code.startswith("python"):
                code = code[6:]
        return code.strip()
