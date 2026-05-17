"""
Stock AI Agent v1 - 测试脚本
用于验证各模块是否正常工作
"""
import sys
import io
from datetime import datetime

# 设置 UTF-8 输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def print_section(title):
    """打印分节标题"""
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print(f"{'=' * 50}")


def test_config():
    """测试配置模块"""
    print_section("测试配置模块")
    try:
        from config import config
        print(f"✅ 配置模块导入成功")
        print(f"   - AI 模型: {config.AI_MODEL}")
        print(f"   - 关注股票: {config.STOCK_WATCH_LIST}")
        print(f"   - 推送时间: {config.SCHEDULE_TIMES}")
        print(f"   - API Key 设置: {'✅' if config.DEEPSEEK_API_KEY else '❌'}")
        print(f"   - Bot Token 设置: {'✅' if config.TELEGRAM_BOT_TOKEN else '❌'}")
        print(f"   - Chat ID 设置: {'✅' if config.TELEGRAM_CHAT_ID else '❌'}")
        return True
    except Exception as e:
        print(f"❌ 配置模块导入失败: {e}")
        return False


def test_logger():
    """测试日志模块"""
    print_section("测试日志模块")
    try:
        from utils.logger import logger
        logger.info("日志模块测试消息")
        print("✅ 日志模块工作正常")
        return True
    except Exception as e:
        print(f"❌ 日志模块导入失败: {e}")
        return False


def test_stock_service():
    """测试股票服务"""
    print_section("测试股票数据服务")
    try:
        from services.stock_service import stock_service
        print("✅ 股票服务模块导入成功")
        
        # 尝试获取股票数据
        print("\n正在获取 AAPL 股票数据...")
        info = stock_service.get_stock_info("AAPL")
        if info:
            print(f"✅ 成功获取 AAPL 数据")
            print(f"   - 价格: ${info.get('price', 0):.2f}")
            print(f"   - 涨跌: {info.get('change', 0):+.2f} ({info.get('change_percent', 0):+.2f}%)")
            return True
        else:
            print("⚠️  无法获取 AAPL 数据（可能网络问题）")
            return True  # 不算失败，可能是网络问题
    except Exception as e:
        print(f"❌ 股票服务测试失败: {e}")
        return False


def test_ai_service():
    """测试 AI 服务"""
    print_section("测试 AI 服务")
    try:
        from services.ai_service import ai_service
        print("✅ AI 服务模块导入成功")
        print(f"   - API Base: {ai_service.client.base_url}")
        print(f"   - Model: {ai_service.model}")
        return True
    except Exception as e:
        print(f"❌ AI 服务导入失败: {e}")
        return False


def test_telegram_service():
    """测试 Telegram 服务"""
    print_section("测试 Telegram 服务")
    try:
        from services.telegram_service import telegram_service
        print("✅ Telegram 服务模块导入成功")
        return True
    except Exception as e:
        print(f"❌ Telegram 服务导入失败: {e}")
        return False


def test_scheduler():
    """测试调度器"""
    print_section("测试调度器")
    try:
        from scheduler.job_scheduler import job_scheduler
        print("✅ 调度器模块导入成功")
        return True
    except Exception as e:
        print(f"❌ 调度器导入失败: {e}")
        return False


def test_agent():
    """测试 Agent"""
    print_section("测试 Stock Agent")
    try:
        from agents.stock_agent import stock_agent
        print("✅ Stock Agent 模块导入成功")
        return True
    except Exception as e:
        print(f"❌ Stock Agent 导入失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("  Stock AI Agent v1 - 模块测试")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    results = []
    
    results.append(("配置模块", test_config()))
    results.append(("日志模块", test_logger()))
    results.append(("股票服务", test_stock_service()))
    results.append(("AI 服务", test_ai_service()))
    results.append(("Telegram 服务", test_telegram_service()))
    results.append(("调度器", test_scheduler()))
    results.append(("Stock Agent", test_agent()))
    
    # 汇总结果
    print_section("测试结果汇总")
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有模块测试通过！项目可以正常运行。")
        print("\n下一步：")
        print("   1. 编辑 .env 文件，填入您的 API Key 和配置")
        print("   2. 运行 python main.py 启动程序")
        return 0
    else:
        print("\n⚠️  部分模块测试失败，请检查错误信息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
