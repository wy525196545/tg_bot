"""
股票 AI Agent 模块
"""
from typing import Dict, Optional, List
from services.stock_service import stock_service
from services.ai_service import ai_service
from services.telegram_service import telegram_service
from utils.logger import logger


class StockAgent:
    """股票 AI Agent - 核心分析引擎"""
    
    def __init__(self):
        self.stock_service = stock_service
        self.ai_service = ai_service
        self.telegram_service = telegram_service
        logger.info("StockAgent 初始化完成")
    
    def get_stock_quote(self, symbol: str) -> Dict:
        """
        获取股票报价
        
        Args:
            symbol: 股票代码
            
        Returns:
            股票信息字典
        """
        logger.info(f"获取股票报价: {symbol}")
        return self.stock_service.get_stock_info(symbol)
    
    def analyze_stock(self, symbol: str, include_technical: bool = True) -> Optional[Dict]:
        """
        全面分析股票
        
        Args:
            symbol: 股票代码
            include_technical: 是否包含技术分析
            
        Returns:
            包含股票信息和分析结果的字典
        """
        logger.info(f"开始分析股票: {symbol}")
        
        # 获取股票基本信息
        stock_info = self.stock_service.get_stock_info(symbol)
        if not stock_info:
            return None
        
        # 获取技术指标
        technical = None
        if include_technical:
            technical = self.stock_service.calculate_technical_indicators(symbol)
        
        # AI 分析
        analysis = self.ai_service.analyze_stock(stock_info, technical)
        
        return {
            "stock_info": stock_info,
            "technical": technical,
            "analysis": analysis
        }
    
    def generate_report(self, symbols: Optional[List[str]] = None) -> Dict:
        """
        生成股票分析报告
        
        Args:
            symbols: 股票代码列表，默认使用配置中的列表
            
        Returns:
            报告结果
        """
        if symbols is None:
            symbols = [s.strip() for s in config.STOCK_WATCH_LIST]
        
        logger.info(f"生成报告: {symbols}")
        
        results = []
        for symbol in symbols:
            result = self.analyze_stock(symbol)
            if result:
                results.append(result)
        
        if not results:
            return {"success": False, "message": "无有效股票数据"}
        
        # 生成综合报告
        stocks_data = [r['stock_info'] for r in results]
        daily_report = self.ai_service.generate_daily_report(stocks_data)
        
        return {
            "success": True,
            "individual_results": results,
            "daily_report": daily_report,
            "timestamp": datetime.now().isoformat()
        }
    
    async def send_analysis_to_telegram(self, symbol: str) -> bool:
        """分析股票并推送到 Telegram"""
        try:
            result = self.analyze_stock(symbol)
            if not result:
                await self.telegram_service.send_message(f"❌ 无法分析股票: {symbol}")
                return False
            
            return await self.telegram_service.send_stock_analysis(
                result['stock_info'],
                result['analysis']
            )
        except Exception as e:
            logger.error(f"推送分析失败: {e}")
            return False
    
    async def send_daily_to_telegram(self) -> bool:
        """发送每日报告到 Telegram"""
        try:
            report = self.generate_report()
            if not report.get('success'):
                await self.telegram_service.send_message("❌ 生成报告失败")
                return False
            
            # 发送综合报告
            message = f"📈 *每日市场简报*\n\n{report['daily_report']}"
            
            # 添加个股摘要
            for result in report['individual_results']:
                info = result['stock_info']
                symbol = info.get('symbol', 'N/A')
                price = info.get('price', 0)
                change = info.get('change_percent', 0)
                emoji = "📈" if change >= 0 else "📉"
                message += f"\n{emoji} {symbol}: ${price:.2f} ({'+' if change >= 0 else ''}{change:.2f}%)"
            
            return await self.telegram_service.send_message(message)
        except Exception as e:
            logger.error(f"发送每日报告失败: {e}")
            return False


# 导入 datetime
from datetime import datetime
# 导入 config
from config import config

# 全局 Agent 实例
stock_agent = StockAgent()
