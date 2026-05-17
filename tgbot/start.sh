#!/bin/bash

echo "================================================"
echo "    Stock AI Agent v1 - 启动脚本"
echo "================================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python，请先安装 Python 3.8+"
    exit 1
fi

echo "[1/4] 检查依赖包..."
if ! python3 -c "import openai" &> /dev/null; then
    echo "[提示] 正在安装依赖包..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖安装失败"
        exit 1
    fi
fi

echo "[2/4] 检查配置文件..."
if [ ! -f ".env" ]; then
    echo "[提示] 未检测到 .env 文件，正在创建..."
    cp .env.example .env
    echo ""
    echo "[重要] 请编辑 .env 文件，填入您的配置："
    echo "  - DEEPSEEK_API_KEY"
    echo "  - TELEGRAM_BOT_TOKEN"
    echo "  - TELEGRAM_CHAT_ID"
    echo ""
    echo "按 Enter 继续..."
    read
fi

echo "[3/4] 验证配置..."
python3 -c "from config import config; exit(0 if config.validate() else 1)"
if [ $? -ne 0 ]; then
    echo "[错误] 配置验证失败，请检查 .env 文件"
    exit 1
fi

echo "[4/4] 启动程序..."
echo ""
echo "================================================"
python3 main.py
