"""
日志工具模块
"""
import logging
import sys
from datetime import datetime
from pathlib import Path
from config import config


class Logger:
    """日志管理器"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self):
        """设置日志器"""
        self._logger = logging.getLogger("StockAIAgent")
        self._logger.setLevel(getattr(logging, config.LOG_LEVEL))
        
        # 避免重复添加 handler
        if self._logger.handlers:
            return
        
        # 日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
        
        # 文件处理器
        try:
            file_handler = logging.FileHandler(
                config.LOG_FILE,
                encoding='utf-8',
                mode='a'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
        except Exception as e:
            self._logger.warning(f"无法创建日志文件: {e}")
    
    def debug(self, msg: str):
        self._logger.debug(msg)
    
    def info(self, msg: str):
        self._logger.info(msg)
    
    def warning(self, msg: str):
        self._logger.warning(msg)
    
    def error(self, msg: str):
        self._logger.error(msg)
    
    def critical(self, msg: str):
        self._logger.critical(msg)


# 全局日志实例
logger = Logger()
