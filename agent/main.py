"""入口: 启动 Agent"""

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
    print(f"已加载偏好: {prefs}")

    while True:
        try:
            requirement = input("\n请输入你的需求(输入 q 退出): ").strip()
        except EOFError:
            print("\n收到 EOF, 退出程序")
            break
        except KeyboardInterrupt:
            print("\n收到中断信号, 退出程序")
            break

        if requirement.lower() == "q":
            print("再见!")
            break
        if not requirement:
            print("需求不能为空, 请重新输入")
            continue

        print("\n开始运行...\n")
        initial_state = {
            "requirement": requirement,
            "code": "",
            "review": "",
            "iteration": 0,
            "review_history": [],
            "review_summary": "",
            "preferences": prefs,
            "execution_result": {},
            "next": "",
            "supervisor_instructions": "",
        }

        app = build_graph()
        result = app.invoke(initial_state)

        print("=" * 50)
        print("最终代码:")
        print("=" * 50)
        print(result["code"])
        print(f"\n共循环了 {result['iteration']} 次")


if __name__ == "__main__":
    main()
