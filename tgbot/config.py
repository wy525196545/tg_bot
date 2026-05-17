"""
配置管理模块
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Config:
    """应用配置类"""
    
    # DeepSeek API 配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"
    AI_MODEL = os.getenv("AI_MODEL", "deepseek-chat")
    AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
    AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "1000"))
    
    # Telegram 配置
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
    
    # 股票配置
    STOCK_WATCH_LIST = os.getenv("STOCK_WATCH_LIST", "600519.SS,601318.SS,0700.HK,000858.SZ").split(",")
    SCHEDULE_TIMES = os.getenv("SCHEDULE_TIMES", "09:25,15:30").split(",")
    TIMEZONE = os.getenv("TIMEZONE", "Asia/Shanghai")
    
    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = "stock_agent.log"
    
    @classmethod
    def validate(cls) -> bool:
        """验证必需配置项"""
        errors = []
        
        if not cls.DEEPSEEK_API_KEY:
            errors.append("DEEPSEEK_API_KEY 未设置")
        
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN 未设置")
        
        if not cls.TELEGRAM_CHAT_ID:
            errors.append("TELEGRAM_CHAT_ID 未设置")
        
        if errors:
            print("⚠️  配置验证失败:")
            for error in errors:
                print(f"  - {error}")
            print("\n请复制 .env.example 为 .env 并填入正确的配置")
            return False
        
        return True


# 全局配置实例
config = Config()
