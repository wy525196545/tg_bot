"""
DeepSeek AI 服务模块
"""
import json
from typing import Dict, Optional
from openai import OpenAI
from config import config
from utils.logger import logger


class AIService:
    """DeepSeek AI 服务"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url=config.DEEPSEEK_API_BASE
        )
        self.model = config.AI_MODEL
        self.temperature = config.AI_TEMPERATURE
        self.max_tokens = config.AI_MAX_TOKENS
    
    def analyze_stock(self, stock_info: Dict, technical_indicators: Optional[Dict] = None) -> str:
        """
        使用 DeepSeek AI 分析股票
        
        Args:
            stock_info: 股票基本信息
            technical_indicators: 技术指标 (可选)
            
        Returns:
            AI 分析结果文本
        """
        if not stock_info:
            return "❌ 无法分析：股票数据不可用"
        
        # 构建分析提示词
        prompt = self._build_analysis_prompt(stock_info, technical_indicators)
        
        try:
            logger.info(f"调用 DeepSeek AI 分析股票: {stock_info.get('symbol')}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """你是一位专业的A股/港股分析师，拥有10年以上的中国市场投资经验。
你的分析风格客观、专业、简洁。你会：
1. 结合技术面和基本面进行分析
2. 关注政策面对A股的影响
3. 提供明确但谨慎的投资建议
4. 适当提示风险
5. 用简洁易懂的语言解释复杂的金融概念

请用中文回复，格式清晰，重点突出。"""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            result = response.choices[0].message.content
            logger.info(f"AI 分析完成: {stock_info.get('symbol')}")
            return result
            
        except Exception as e:
            logger.error(f"AI 分析失败: {e}")
            return f"❌ AI 分析失败: {str(e)}"
    
    def generate_daily_report(self, stocks_data: list) -> str:
        """
        生成每日股票简报
        
        Args:
            stocks_data: 股票数据列表
            
        Returns:
            每日报告文本
        """
        if not stocks_data:
            return "❌ 无股票数据可分析"
        
        # 构建报告提示词
        prompt = "请为以下股票生成今日市场简报，包括整体趋势、重点关注和建议：\n\n"
        for stock in stocks_data:
            prompt += f"• {stock.get('symbol')}: ${stock.get('price', 0):.2f} "
            prompt += f"({'+' if stock.get('change', 0) >= 0 else ''}{stock.get('change_percent', 0):.2f}%)\n"
        
        try:
            logger.info("生成每日市场简报")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """你是一位专业的财经分析师，负责生成简洁的市场日报。
你的报告应该：
1. 总结整体市场情绪
2. 指出今日亮点和风险
3. 提供综合投资建议
4. 保持专业但易懂

请用中文回复，格式清晰，长度适中(200-400字)。"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            logger.info("每日简报生成完成")
            return result
            
        except Exception as e:
            logger.error(f"生成每日简报失败: {e}")
            return f"❌ 生成每日简报失败: {str(e)}"
    
    def _build_analysis_prompt(self, stock_info: Dict, technical: Optional[Dict]) -> str:
        """构建分析提示词"""
        
        symbol = stock_info.get('symbol', 'N/A')
        name = stock_info.get('name', 'Unknown')
        price = stock_info.get('price', 0)
        change = stock_info.get('change', 0)
        change_pct = stock_info.get('change_percent', 0)
        currency = stock_info.get('currency', 'USD')
        pe = stock_info.get('pe_ratio', 0)
        market_cap = stock_info.get('market_cap', 0)
        
        currency_symbol = "$" if currency == "USD" else ("¥" if currency == "CNY" else "")
        
        prompt = f"""请分析以下股票：

**股票代码**: {symbol}
**公司名称**: {name}
**当前价格**: {currency_symbol}{price:.2f}
**今日涨跌**: {'+' if change >= 0 else ''}{currency_symbol}{change:.2f} ({'+' if change_pct >= 0 else ''}{change_pct:.2f}%)
**开盘价**: {currency_symbol}{stock_info.get('open', 0):.2f}
**最高价**: {currency_symbol}{stock_info.get('high', 0):.2f}
**最低价**: {currency_symbol}{stock_info.get('low', 0):.2f}
**成交量**: {stock_info.get('volume', 0):,}
**52周最高**: {currency_symbol}{stock_info.get('52w_high', 0):.2f}
**52周最低**: {currency_symbol}{stock_info.get('52w_low', 0):.2f}"""
        
        if pe:
            prompt += f"\n**市盈率(PE)**: {pe:.2f}"
        
        if market_cap:
            if market_cap > 1e12:
                prompt += f"\n**市值**: {currency_symbol}{market_cap/1e12:.2f}万亿"
            else:
                prompt += f"\n**市值**: {currency_symbol}{market_cap/1e9:.2f}十亿"
        
        if technical:
            prompt += f"\n\n**技术指标**:"
            prompt += f"\n• 5日均线: {currency_symbol}{technical.get('sma_5', 0):.2f}" if technical.get('sma_5') else ""
            prompt += f"\n• 10日均线: {currency_symbol}{technical.get('sma_10', 0):.2f}" if technical.get('sma_10') else ""
            prompt += f"\n• 20日均线: {currency_symbol}{technical.get('sma_20', 0):.2f}" if technical.get('sma_20') else ""
            prompt += f"\n• RSI(14): {technical.get('rsi', 0):.2f}" if technical.get('rsi') else ""
            prompt += f"\n• 趋势: {technical.get('trend', '不确定')}"
        
        prompt += "\n\n请从技术面和基本面两个角度进行分析，并给出明确的投资建议（买入/持有/卖出）。"
        
        return prompt


# 全局服务实例
ai_service = AIService()
