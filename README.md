# Dawn Agent

基于 LangGraph 的 Coder + Reviewer 双 Agent 系统

## 项目结构

```
dawn-agent/
├── agent/                  # 核心业务包
│   ├── core/
│   │   ├── ports/          # 抽象接口（契约定义）
│   │   │   ├── storage.py
│   │   │   ├── session.py
│   │   │   └── monitor.py
│   │   ├── base_agent.py
│   │   ├── base_tool.py
│   │   └── exceptions.py
│   ├── schemas/            # 数据结构定义
│   ├── nodes/              # Agent 节点
│   │   ├── coder.py
│   │   ├── reviewer.py
│   │   └── summarizer.py
│   ├── graph/              # 图定义和流程控制
│   ├── tools/              # 工具函数
│   ├── memory/             # 长期记忆
│   ├── session/            # 会话管理（待扩展）
│   ├── skills/             # 可复用技能（待扩展）
│   └── main.py             # Python 入口
│
├── plugins/                # 可选插件（实现 ports 接口）
│   ├── storage/            # Redis、PostgreSQL
│   ├── monitoring/         # LangSmith
│   └── middleware/         # 认证、限流
│
├── config/                 # 全局配置、LLM 工厂
├── scripts/                # Shell 脚本
├── tests/                  # 测试
├── docs/                   # 文档
├── frontend/               # 前端（待扩展）
├── backend/                # API 服务（待扩展）
└── mcp/                    # MCP 集成（待扩展）
```

## 快速开始

```bash
export DASHSCOPE_API_KEY="你的Key"
uv run python agent/main.py
# 或者
./scripts/start.sh
```

## 架构设计

- **Ports & Plugins 模式**：`agent/core/ports/` 定义接口契约，`plugins/` 实现增强功能
- **没有 plugins 也能跑**：agent 内置默认实现
- **有了 plugins 功能增强**：注入 Redis、LangSmith 等，agent 代码不用改

## 技术栈

- LangGraph：Agent 编排
- 千问（云端）：Coder
- Ollama qwen3:8b（本地）：Reviewer
- SQLite：记忆持久化
- Pydantic：结构化输出
