"""
Stock AI Agent v1 - 主程序入口
自动股票分析 + Telegram 推送 + 定时任务
"""
import asyncio
import logging
from datetime import datetime
from pathlib import Path

from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

from config import config
from utils.logger import logger
from agents.stock_agent import stock_agent
from services.stock_service import stock_service
from services.telegram_service import telegram_service
from scheduler.job_scheduler import job_scheduler


# ==================== Telegram Bot Handlers ====================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    welcome = """
🤖 *欢迎使用 Stock AI Agent v1*

这是一个自动化的A股/港股分析助手，可以为您提供：

📊 *功能列表*
• /stock <代码> - 查询股票信息
• /analyze <代码> - AI 分析股票
• /subscribe - 订阅每日推送
• /unsubscribe - 取消订阅  
• /status - 查看订阅状态
• /help - 获取帮助

💡 *使用示例*
• /stock 600519.SS - 查询茅台
• /analyze 601318.SS - 分析中国平安

🔔 *每日推送时间*
09:25 (开盘前) | 15:30 (收盘后)

输入股票代码开始分析吧！
"""
    await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /help 命令"""
    help_text = """
📖 *使用帮助*

*股票查询*
`/stock 600519.SS` - 查询贵州茅台
`/stock 601318.SS` - 查询中国平安
`/stock 0700.HK` - 查询腾讯控股

*AI 分析*
`/analyze 600519.SS` - 获取茅台深度分析报告
`/analyze 0700.HK` - 获取腾讯深度分析报告

*订阅管理*
`/subscribe` - 开启每日自动推送
`/unsubscribe` - 取消每日推送
`/status` - 查看当前订阅状态

*支持的股票代码*
• A股-上交所: 600519.SS (贵州茅台)
• A股-深交所: 000858.SZ (五粮液)
• 港股: 0700.HK (腾讯)
• 美股: 98880.HK (阿里巴巴)
"""
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


async def cmd_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /stock 命令 - 查询股票信息"""
    if not context.args:
        await update.message.reply_text(
            "❌ 请提供股票代码\n用法: `/stock AAPL`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    symbol = context.args[0].upper()
    logger.info(f"查询股票: {symbol}")
    
    await update.message.reply_text(f"🔍 正在查询 {symbol}...")
    
    stock_info = stock_service.get_stock_info(symbol)
    if stock_info:
        summary = stock_service.format_stock_summary(stock_info)
        await update.message.reply_text(summary, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(f"❌ 无法获取 {symbol} 的数据，请检查代码是否正确")


async def cmd_analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /analyze 命令 - AI 分析股票"""
    if not context.args:
        await update.message.reply_text(
            "❌ 请提供股票代码\n用法: `/analyze AAPL`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    symbol = context.args[0].upper()
    logger.info(f"AI 分析股票: {symbol}")
    
    await update.message.reply_text(f"🤖 正在分析 {symbol}，请稍候...")
    
    # 发送 loading 消息
    loading_msg = await update.message.reply_text("⏳ AI 正在思考中...")
    
    # 执行分析
    result = stock_agent.analyze_stock(symbol)
    
    if not result:
        await loading_msg.edit_text(f"❌ 分析失败：无法获取 {symbol} 的数据")
        return
    
    # 构建分析报告
    stock_info = result['stock_info']
    analysis = result['analysis']
    
    header = f"📊 *{symbol} AI 分析报告*\n━━━━━━━━━━━━━━━━━━━━\n"
    
    # 基本信息
    price = stock_info.get('price', 0)
    change = stock_info.get('change', 0)
    change_pct = stock_info.get('change_percent', 0)
    emoji = "📈" if change >= 0 else "📉"
    sign = "+" if change >= 0 else ""
    
    basic_info = f"""
{emoji} **{stock_info.get('name', symbol)}**

💰 价格: ${price:.2f}
{sign}${change:.2f} ({sign}{change_pct:.2f}%)

📈 今日数据:
• 开盘: ${stock_info.get('open', 0):.2f}
• 最高: ${stock_info.get('high', 0):.2f}
• 最低: ${stock_info.get('low', 0):.2f}
• 成交量: {stock_info.get('volume', 0):,}
"""
    
    # 技术指标
    technical = result.get('technical')
    tech_info = ""
    if technical:
        sma_5_str = f"${technical.get('sma_5', 0):.2f}" if technical.get('sma_5') else "N/A"
        sma_10_str = f"${technical.get('sma_10', 0):.2f}" if technical.get('sma_10') else "N/A"
        rsi_str = f"{technical.get('rsi', 0):.1f}" if technical.get('rsi') else "N/A"
        tech_info = f"""
📉 技术指标:
• 5日均线: {sma_5_str}
• 10日均线: {sma_10_str}
• RSI(14): {rsi_str}
• 趋势: {technical.get('trend', '不确定')}
"""
    
    # AI 分析
    ai_analysis = f"""
🤖 *AI 分析结论*:

{analysis}
"""
    
    footer = f"""
━━━━━━━━━━━━━━━━━━━━
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    full_report = header + basic_info + tech_info + ai_analysis + footer
    
    await loading_msg.edit_text(full_report, parse_mode=ParseMode.MARKDOWN)


async def cmd_subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /subscribe 命令 - 订阅每日推送"""
    chat_id = str(update.effective_chat.id)
    
    if telegram_service.is_subscribed(chat_id):
        await update.message.reply_text("✅ 您已经在订阅列表中，无需重复订阅")
    else:
        telegram_service.add_subscriber(chat_id)
        await update.message.reply_text(
            "✅ *订阅成功！*\n\n您将收到每日市场简报和重点股票分析。\n\n推送时间: 09:25 (开盘前) | 15:30 (收盘后)",
            parse_mode=ParseMode.MARKDOWN
        )


async def cmd_unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /unsubscribe 命令 - 取消订阅"""
    chat_id = str(update.effective_chat.id)
    
    if not telegram_service.is_subscribed(chat_id):
        await update.message.reply_text("ℹ️ 您还未订阅每日推送")
    else:
        telegram_service.remove_subscriber(chat_id)
        await update.message.reply_text("✅ 已取消订阅每日推送")


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /status 命令 - 查看状态"""
    chat_id = str(update.effective_chat.id)
    is_subscribed = telegram_service.is_subscribed(chat_id)
    watch_list = ", ".join(config.STOCK_WATCH_LIST)
    
    status_text = f"""
📋 *订阅状态*

🔔 每日推送: {'✅ 已订阅' if is_subscribed else '❌ 未订阅'}
📊 关注股票: {watch_list}
⏰ 推送时间: 09:25, 15:30

💡 输入 /subscribe 开启每日推送
"""
    await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)


# ==================== 定时任务函数 ====================

async def daily_report_job():
    """每日报告定时任务"""
    logger.info("执行每日报告任务")
    await stock_agent.send_daily_to_telegram()


# ==================== 主程序 ====================

def setup_telegram_bot():
    """设置 Telegram Bot"""
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # 添加命令处理器
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("stock", cmd_stock))
    app.add_handler(CommandHandler("analyze", cmd_analyze))
    app.add_handler(CommandHandler("subscribe", cmd_subscribe))
    app.add_handler(CommandHandler("unsubscribe", cmd_unsubscribe))
    app.add_handler(CommandHandler("status", cmd_status))
    
    # 设置命令菜单
    async def post_init(app: Application):
        commands = [
            BotCommand("start", "启动 Bot"),
            BotCommand("help", "获取帮助"),
            BotCommand("stock", "查询股票"),
            BotCommand("analyze", "AI 分析"),
            BotCommand("subscribe", "订阅推送"),
            BotCommand("unsubscribe", "取消订阅"),
            BotCommand("status", "查看状态"),
        ]
        await app.bot.set_my_commands(commands)
        logger.info("Telegram Bot 命令菜单已设置")
    
    app.post_init = post_init
    
    return app


def setup_scheduler():
    """设置定时任务"""
    # 添加每日报告任务
    for time_str in config.SCHEDULE_TIMES:
        try:
            hour, minute = map(int, time_str.strip().split(':'))
            job_scheduler.add_daily_job(
                daily_report_job,
                f"daily_report_{time_str.replace(':', '')}",
                hour,
                minute
            )
        except ValueError:
            logger.warning(f"无效的时间格式: {time_str}")


def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("Stock AI Agent v1 启动中...")
    logger.info("=" * 50)
    
    # 验证配置
    if not config.validate():
        logger.error("配置验证失败，请检查 .env 文件")
        return
    
    # 设置定时任务
    setup_scheduler()
    job_scheduler.start()
    
    # 设置并启动 Telegram Bot
    app = setup_telegram_bot()
    
    logger.info("=" * 50)
    logger.info("✅ Stock AI Agent v1 已启动！")
    logger.info(f"📊 关注股票: {', '.join(config.STOCK_WATCH_LIST)}")
    logger.info(f"⏰ 推送时间: {', '.join(config.SCHEDULE_TIMES)}")
    logger.info("=" * 50)
    logger.info("📱 Telegram Bot 已就绪，等待消息...")
    logger.info("按 Ctrl+C 停止程序")
    logger.info("=" * 50)
    
    # 启动 Bot
    try:
        app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        logger.info("收到停止信号，正在关闭...")
        job_scheduler.stop()
        logger.info("程序已退出")


if __name__ == "__main__":
    main()
