# 自动股票 AI Agent v1 - 项目规范

## 1. 项目概述

- **项目名称**: Stock AI Agent v1
- **项目类型**: Python 自动化脚本
- **核心功能**: 自动获取股票数据，通过 DeepSeek AI 分析，向 Telegram 推送股票分析和交易建议
- **目标用户**: 股票投资者，需要每日自动化的市场分析和提醒

## 2. 技术架构

### 核心依赖
- **AI 模型**: DeepSeek API (通过 OpenAI 兼容接口)
- **股票数据**: yfinance (Yahoo Finance 免费数据源)
- **消息推送**: Telegram Bot API
- **定时任务**: APScheduler
- **HTTP 客户端**: requests

### 项目结构
```
stock-ai-agent/
├── config.py           # 配置文件
├── main.py             # 主程序入口
├── agents/
│   └── stock_agent.py   # 股票分析 AI Agent
├── services/
│   ├── stock_service.py    # 股票数据服务
│   ├── ai_service.py       # DeepSeek AI 服务
│   └── telegram_service.py # Telegram 推送服务
├── scheduler/
│   └── job_scheduler.py    # 定时任务调度器
├── utils/
│   └── logger.py           # 日志工具
├── requirements.txt        # 依赖列表
├── .env.example           # 环境变量示例
└── README.md              # 项目说明
```

## 3. 功能列表

### 3.1 股票数据获取
- 支持获取单只股票或多只股票数据
- 获取数据包括：当前价格、涨跌幅、开盘价、收盘价、最高价、最低价、成交量
- 支持获取历史 K 线数据（1天、1周、1月）
- 使用 yfinance 库获取 Yahoo Finance 数据

### 3.2 AI 分析引擎
- 使用 DeepSeek API 进行股票分析
- 支持技术分析：趋势判断、支撑位/压力位识别
- 支持基本面分析：PE、PB、市值等指标解读
- 生成交易建议：买入/卖出/持有
- 输出格式化分析报告

### 3.3 Telegram 推送
- 通过 Bot API 推送消息
- 支持文本消息格式
- 支持 Markdown 格式化
- 包含股票代码、价格、分析和建议

### 3.4 定时任务
- 支持每日定时推送（开盘前/收盘后）
- 支持自定义推送时间
- 支持手动触发分析
- 使用 APScheduler 实现

### 3.5 交互命令
- `/start` - 启动 Bot，显示欢迎信息
- `/stock <代码>` - 查询指定股票
- `/analyze <代码>` - AI 分析指定股票
- `/subscribe` - 订阅每日推送
- `/unsubscribe` - 取消订阅
- `/status` - 查看订阅状态
- `/help` - 获取帮助信息

## 4. 配置项

### 环境变量
```
DEEPSEEK_API_KEY=your_deepseek_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
STOCK_WATCH_LIST=AAPL,TSLA,GOOGL,MSFT  # 关注的股票列表
SCHEDULE_TIME=09:25                     # 每日推送时间
TIMEZONE=Asia/Shanghai                  # 时区设置
```

### 可配置参数
- 股票列表
- 推送时间
- 分析深度
- 消息格式

## 5. 输出格式

### Telegram 推送示例
```
📊 股票AI分析报告 - 2026-05-17 09:25

🏷️ 股票: AAPL (Apple Inc.)
💰 当前价格: $189.45
📈 今日涨跌: +2.35 (+1.26%)

📉 技术指标:
• 5日均线: $187.20 (趋势向上)
• 10日均线: $185.50
• RSI(14): 58.4 (中性区间)

🤖 AI 分析:
苹果公司近期表现强劲，财报超预期，iPhone需求稳定。

💡 建议: 持有为主，可考虑在$185附近适量加仓

⏰ 下次更新: 明日 09:25
```

## 6. 错误处理

- API 请求失败重试机制（最多3次）
- 股票代码无效提示
- 网络异常处理
- 日志记录完整错误信息

## 7. 部署要求

- Python 3.8+
- 稳定的网络连接
- DeepSeek API Key
- Telegram Bot Token

## 8. 验收标准

1. ✅ 程序可独立运行
2. ✅ 可获取实时股票数据
3. ✅ AI 分析可正常调用 DeepSeek
4. ✅ Telegram 消息可正常推送
5. ✅ 定时任务可按设定时间执行
6. ✅ Telegram 命令可正常响应
7. ✅ 错误信息有友好提示
