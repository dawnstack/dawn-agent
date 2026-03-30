"""统一处理 LLM 输出清理"""


def clean_code(text: str) -> str:
    """清理 LLM 返回的代码，去掉 markdown 代码块"""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("python"):
            text = text[6:]
    return text.strip()


def clean_json(text: str) -> str:
    """清理 LLM 返回的 JSON，去掉 markdown 包裹"""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()