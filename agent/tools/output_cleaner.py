"""统一处理 LLM 输出清理"""


def clean_code(text: str) -> str:
    """清理 LLM 返回的代码, 去掉 markdown 代码块"""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("python"):
            text = text[6:]
    return text.strip()


def clean_json(text: str) -> str:
    """清理 LLM 返回的 JSON, 去掉 markdown 包裹"""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()


def extract_json_object(text: str) -> str:
    """从混杂文本中提取最外层 JSON object"""
    cleaned = clean_json(text)
    start = cleaned.find("{")
    if start == -1:
        raise ValueError("No JSON object start found")

    depth = 0
    in_string = False
    escape = False

    for index in range(start, len(cleaned)):
        char = cleaned[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return cleaned[start : index + 1]

    raise ValueError("No complete JSON object found")
