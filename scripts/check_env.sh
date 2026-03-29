#!/bin/bash
# 环境检查
echo "🔍 检查环境..."
python3 --version
echo "DASHSCOPE_API_KEY: ${DASHSCOPE_API_KEY:0:8}..."
ollama list
echo "✅ 环境检查完成"
