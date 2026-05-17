from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from config import BOT_TOKEN, TARGET_STOCKS
from tools.stock import get_stock
from agent.analyst import analyze_stock

import asyncio
