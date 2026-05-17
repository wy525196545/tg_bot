"""
Telegram 推送服务模块
"""
import asyncio
from typing import Optional
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from config import config
from utils.logger import logger


class TelegramService:
    """Telegram Bot 服务"""
    
    def __init__(self):
        self.bot_token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.app = None
        self._subscribers = set()
        
    async def send_message(self, text: str, parse_mode: str = ParseMode.MARKDOWN) -> bool:
        """
        发送消息到 Telegram
        
        Args:
            text: 消息内容
            parse_mode: 解析模式 (MARKDOWN, HTML)
            
        Returns:
            是否发送成功
        """
        if not self.chat_id:
            logger.error("Telegram CHAT_ID 未配置")
            return False
        
        try:
            from telegram import Bot
            bot = Bot(token=self.bot_token)
            await bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode=parse_mode
            )
            logger.info(f"Telegram 消息发送成功")
            return True
        except Exception as e:
            logger.error(f"Telegram 消息发送失败: {e}")
            return False
    
    async def send_stock_analysis(self, stock_info: dict, analysis: str) -> bool:
        """发送股票分析报告"""
        from services.stock_service import stock_service
        
        # 构建消息
        stock_summary = stock_service.format_stock_summary(stock_info)
        
        message = f"""
📊 *股票AI分析报告*
━━━━━━━━━━━━━━━━━━━━

{stock_summary}

🤖 *AI 分析结论*:

{analysis}
"""
        
        return await self.send_message(message)
    
    async def send_daily_report(self, report: str) -> bool:
        """发送每日市场简报"""
        message = f"📈 *每日市场简报*\n━━━━━━━━━━━━━━━━━━━━\n{report}"
        return await self.send_message(message)
    
    async def setup_commands(self):
        """设置 Bot 命令列表"""
        try:
            from telegram import Bot
            bot = Bot(token=self.bot_token)
            
            commands = [
                BotCommand("start", "启动 Bot"),
                BotCommand("help", "获取帮助"),
                BotCommand("stock", "查询股票信息\n用法: /stock AAPL"),
                BotCommand("analyze", "AI 分析股票\n用法: /analyze AAPL"),
                BotCommand("subscribe", "订阅每日推送"),
                BotCommand("unsubscribe", "取消订阅"),
                BotCommand("status", "查看订阅状态"),
            ]
            
            await bot.set_my_commands(commands)
            logger.info("Telegram Bot 命令设置成功")
        except Exception as e:
            logger.error(f"设置 Bot 命令失败: {e}")
    
    def add_subscriber(self, chat_id: str):
        """添加订阅者"""
        self._subscribers.add(chat_id)
        logger.info(f"新订阅者: {chat_id}")
    
    def remove_subscriber(self, chat_id: str):
        """移除订阅者"""
        self._subscribers.discard(chat_id)
        logger.info(f"取消订阅: {chat_id}")
    
    def is_subscribed(self, chat_id: str) -> bool:
        """检查是否已订阅"""
        return chat_id in self._subscribers
    
    def get_subscribers(self) -> set:
        """获取所有订阅者"""
        return self._subscribers.copy()


# 全局服务实例
telegram_service = TelegramService()
