"""
股票数据服务模块
"""
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import pandas as pd
from utils.logger import logger


class StockService:
    """股票数据服务"""
    
    def __init__(self):
        self.market_timezones = {
            "US": "America/New_York",
            "CN": "Asia/Shanghai", 
            "HK": "Asia/Hong_Kong",
            "JP": "Asia/Tokyo"
        }
    
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """
        获取股票基本信息
        
        Args:
            symbol: 股票代码 (如 AAPL, TSLA)
            
        Returns:
            股票信息字典，失败返回 None
        """
        try:
            logger.info(f"获取股票信息: {symbol}")
            stock = yf.Ticker(symbol)
            info = stock.info
            
            if not info or 'regularMarketPrice' not in info:
                logger.warning(f"股票 {symbol} 数据不可用")
                return None
            
            result = {
                "symbol": symbol.upper(),
                "name": info.get('shortName', symbol),
                "price": info.get('regularMarketPrice', 0),
                "change": info.get('regularMarketChange', 0),
                "change_percent": info.get('regularMarketChangePercent', 0),
                "open": info.get('regularMarketOpen', 0),
                "high": info.get('regularMarketDayHigh', 0),
                "low": info.get('regularMarketDayLow', 0),
                "volume": info.get('regularMarketVolume', 0),
                "previous_close": info.get('regularMarketPreviousClose', 0),
                "market_cap": info.get('marketCap', 0),
                "pe_ratio": info.get('trailingPE', 0),
                "dividend_yield": info.get('dividendYield', 0),
                "52w_high": info.get('fiftyTwoWeekHigh', 0),
                "52w_low": info.get('fiftyTwoWeekLow', 0),
                "avg_volume": info.get('averageVolume', 0),
                "currency": info.get('currency', 'USD'),
                "exchange": info.get('exchange', 'UNKNOWN'),
                "timestamp": datetime.now().isoformat()
            }
            
            # 获取正确的货币符号
            currency = result['currency']
            if currency == 'CNY':
                currency_symbol = "¥"
            elif currency == 'HKD':
                currency_symbol = "HK$"
            else:
                currency_symbol = "$"
            
            logger.info(f"成功获取 {symbol} 数据: {currency_symbol}{result['price']:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"获取股票 {symbol} 信息失败: {e}")
            return None
    
    def get_historical_data(self, symbol: str, period: str = "1mo") -> Optional[pd.DataFrame]:
        """
        获取股票历史数据
        
        Args:
            symbol: 股票代码
            period: 时间周期 (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, max)
            
        Returns:
            包含历史数据的 DataFrame
        """
        try:
            logger.info(f"获取 {symbol} 历史数据 (周期: {period})")
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)
            
            if df.empty:
                logger.warning(f"股票 {symbol} 无历史数据")
                return None
            
            return df
            
        except Exception as e:
            logger.error(f"获取 {symbol} 历史数据失败: {e}")
            return None
    
    def calculate_technical_indicators(self, symbol: str, period: str = "1mo") -> Optional[Dict]:
        """
        计算技术指标
        
        Args:
            symbol: 股票代码
            period: 时间周期
            
        Returns:
            技术指标字典
        """
        try:
            df = self.get_historical_data(symbol, period)
            if df is None or df.empty:
                return None
            
            # 计算简单移动平均线
            df['SMA_5'] = df['Close'].rolling(window=5).mean()
            df['SMA_10'] = df['Close'].rolling(window=10).mean()
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            
            # 计算 RSI (相对强弱指数)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            df['RSI'] = rsi
            
            # 获取最新值
            latest = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else latest
            
            indicators = {
                "current_price": float(latest['Close']),
                "sma_5": float(latest['SMA_5']) if pd.notna(latest['SMA_5']) else None,
                "sma_10": float(latest['SMA_10']) if pd.notna(latest['SMA_10']) else None,
                "sma_20": float(latest['SMA_20']) if pd.notna(latest['SMA_20']) else None,
                "rsi": float(latest['RSI']) if pd.notna(latest['RSI']) else None,
                "volume": int(latest['Volume']),
                "price_change_1d": float(latest['Close'] - prev['Close']) if len(df) > 1 else 0,
                "price_change_pct_1d": float((latest['Close'] - prev['Close']) / prev['Close'] * 100) if len(df) > 1 and prev['Close'] != 0 else 0
            }
            
            # 趋势判断
            if pd.notna(latest['SMA_5']) and pd.notna(latest['SMA_10']):
                if latest['SMA_5'] > latest['SMA_10']:
                    indicators['trend'] = "上升"
                elif latest['SMA_5'] < latest['SMA_10']:
                    indicators['trend'] = "下降"
                else:
                    indicators['trend'] = "震荡"
            else:
                indicators['trend'] = "不确定"
            
            logger.info(f"计算 {symbol} 技术指标完成")
            return indicators
            
        except Exception as e:
            logger.error(f"计算 {symbol} 技术指标失败: {e}")
            return None
    
    def get_multiple_stocks(self, symbols: List[str]) -> List[Dict]:
        """
        获取多只股票数据
        
        Args:
            symbols: 股票代码列表
            
        Returns:
            股票信息列表
        """
        results = []
        for symbol in symbols:
            info = self.get_stock_info(symbol.strip())
            if info:
                results.append(info)
        return results
    
    def format_stock_summary(self, stock_info: Dict) -> str:
        """格式化股票摘要信息"""
        if not stock_info:
            return "❌ 股票数据不可用"
        
        symbol = stock_info.get('symbol', 'N/A')
        name = stock_info.get('name', 'Unknown')
        price = stock_info.get('price', 0)
        change = stock_info.get('change', 0)
        change_pct = stock_info.get('change_percent', 0)
        currency = stock_info.get('currency', 'CNY')  # 默认人民币
        
        # 涨跌符号
        emoji = "📈" if change >= 0 else "📉"
        sign = "+" if change >= 0 else ""
        
        # 根据货币选择符号
        if currency == 'CNY':
            currency_symbol = "¥"
        elif currency == 'HKD':
            currency_symbol = "HK$"
        else:
            currency_symbol = "$"
        
        summary = f"""
{emoji} **{symbol}** - {name}

💰 价格: {currency_symbol}{price:.2f}
{sign}{currency_symbol}{change:.2f} ({sign}{change_pct:.2f}%)

📊 基本信息:
• 开盘: {currency_symbol}{stock_info.get('open', 0):.2f}
• 最高: {currency_symbol}{stock_info.get('high', 0):.2f}
• 最低: {currency_symbol}{stock_info.get('low', 0):.2f}
• 成交量: {stock_info.get('volume', 0):,}
• 52周最高: {currency_symbol}{stock_info.get('52w_high', 0):.2f}
• 52周最低: {currency_symbol}{stock_info.get('52w_low', 0):.2f}
"""
        
        if stock_info.get('pe_ratio'):
            summary += f"• 市盈率(PE): {stock_info.get('pe_ratio', 0):.2f}\n"
        if stock_info.get('market_cap'):
            cap = stock_info['market_cap']
            if currency == 'CNY':
                # A股使用万亿
                summary += f"• 市值: {currency_symbol}{cap/1e12:.2f}万亿\n"
            else:
                if cap > 1e12:
                    summary += f"• 市值: {currency_symbol}{cap/1e12:.2f}万亿\n"
                elif cap > 1e9:
                    summary += f"• 市值: {currency_symbol}{cap/1e9:.2f}十亿\n"
        
        return summary


# 全局服务实例
stock_service = StockService()
