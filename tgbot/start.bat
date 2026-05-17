@echo off
chcp 65001 >nul
echo ================================================
echo     Stock AI Agent v1 - 启动脚本
echo ================================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [1/4] 检查依赖包...
pip show openai >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo [2/4] 检查配置文件...
if not exist ".env" (
    echo [提示] 未检测到 .env 文件，正在创建...
    copy .env.example .env
    echo.
    echo [重要] 请编辑 .env 文件，填入您的配置：
    echo   - DEEPSEEK_API_KEY
    echo   - TELEGRAM_BOT_TOKEN  
    echo   - TELEGRAM_CHAT_ID
    echo.
    notepad .env
    echo 按任意键继续...
    pause >nul
)

echo [3/4] 验证配置...
python -c "from config import config; exit(0 if config.validate() else 1)"
if errorlevel 1 (
    echo [错误] 配置验证失败，请检查 .env 文件
    pause
    exit /b 1
)

echo [4/4] 启动程序...
echo.
echo ================================================
python main.py
