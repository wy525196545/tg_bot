"""
定时任务调度器模块
"""
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from typing import Callable, List
from config import config
from utils.logger import logger


class JobScheduler:
    """定时任务调度器"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=config.TIMEZONE)
        self._jobs = []
        logger.info(f"调度器初始化完成，时区: {config.TIMEZONE}")
    
    def add_daily_job(self, job_func: Callable, job_id: str, hour: int, minute: int):
        """
        添加每日定时任务
        
        Args:
            job_func: 要执行的函数 (可以是 async 函数)
            job_id: 任务 ID
            hour: 小时 (0-23)
            minute: 分钟 (0-59)
        """
        try:
            trigger = CronTrigger(
                hour=hour,
                minute=minute,
                timezone=config.TIMEZONE
            )
            
            self.scheduler.add_job(
                job_func,
                trigger=trigger,
                id=job_id,
                name=f"Daily Job: {job_id}",
                replace_existing=True
            )
            
            self._jobs.append({
                "id": job_id,
                "type": "daily",
                "time": f"{hour:02d}:{minute:02d}",
                "func": job_func.__name__ if hasattr(job_func, '__name__') else str(job_func)
            })
            
            logger.info(f"添加每日任务 [{job_id}]: {hour:02d}:{minute:02d}")
        except Exception as e:
            logger.error(f"添加每日任务失败 [{job_id}]: {e}")
    
    def add_interval_job(self, job_func: Callable, job_id: str, hours: int = 0, minutes: int = 0):
        """
        添加间隔执行任务
        
        Args:
            job_func: 要执行的函数
            job_id: 任务 ID
            hours: 间隔小时数
            minutes: 间隔分钟数
        """
        try:
            from apscheduler.triggers.interval import IntervalTrigger
            
            trigger = IntervalTrigger(
                hours=hours,
                minutes=minutes,
                timezone=config.TIMEZONE
            )
            
            self.scheduler.add_job(
                job_func,
                trigger=trigger,
                id=job_id,
                name=f"Interval Job: {job_id}",
                replace_existing=True
            )
            
            self._jobs.append({
                "id": job_id,
                "type": "interval",
                "interval": f"{hours}h {minutes}m",
                "func": job_func.__name__ if hasattr(job_func, '__name__') else str(job_func)
            })
            
            interval_str = f"{hours}小时" if hours else ""
            interval_str += f"{minutes}分钟" if minutes else ""
            logger.info(f"添加间隔任务 [{job_id}]: 每{interval_str}")
        except Exception as e:
            logger.error(f"添加间隔任务失败 [{job_id}]: {e}")
    
    def remove_job(self, job_id: str):
        """移除任务"""
        try:
            self.scheduler.remove_job(job_id)
            self._jobs = [j for j in self._jobs if j['id'] != job_id]
            logger.info(f"移除任务: {job_id}")
        except Exception as e:
            logger.error(f"移除任务失败 [{job_id}]: {e}")
    
    def start(self):
        """启动调度器"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("调度器已启动")
            self._print_jobs()
    
    def stop(self):
        """停止调度器"""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            logger.info("调度器已停止")
    
    def _print_jobs(self):
        """打印当前任务列表"""
        if self._jobs:
            logger.info(f"当前任务列表 (共 {len(self._jobs)} 个):")
            for job in self._jobs:
                if job['type'] == 'daily':
                    logger.info(f"  - [{job['id']}] 每日 {job['time']} -> {job['func']}")
                else:
                    logger.info(f"  - [{job['id']}] 每{job['interval']} -> {job['func']}")
        else:
            logger.info("当前无定时任务")
    
    def get_jobs(self) -> List[dict]:
        """获取任务列表"""
        return self._jobs.copy()


# 全局调度器实例
job_scheduler = JobScheduler()
