"""入口：启动 Agent"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.memory.memory import init_db, save_preference, load_preferences
from agent.graph.graph import build_graph


def main():
    # 初始化记忆
    init_db()
    save_preference("code_style", {"type_hints": True, "docstring": True})
    save_preference("preferred_libraries", ["pathlib", "csv"])
    prefs = load_preferences()
    print(f"📚 已加载偏好：{prefs}")

    initial_state = {
        "requirement": "write a function, read a file of CSV, return the average of every column.",
        "code": "",
        "review": "",
        "iteration": 0,
        "review_history": [],
        "review_summary": "",
        "preferences": prefs,
        "execution_result": {},
    }

    app = build_graph()
    result = app.invoke(initial_state)

    print("=" * 50)
    print("✅ 最终代码：")
    print("=" * 50)
    print(result["code"])
    print(f"\n📊 共循环了 {result['iteration']} 次")


if __name__ == "__main__":
    main()
