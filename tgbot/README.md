# 自动股票 AI Agent v1

🤖 基于 DeepSeek AI 的自动化 A股/港股分析助手，支持 Telegram 推送和定时任务。

## 功能特性

- 📊 **股票数据获取** - 实时获取 Yahoo Finance A股/港股数据
- 🤖 **AI 智能分析** - 使用 DeepSeek 模型进行深度技术分析
- 📱 **Telegram 推送** - 支持 Bot 命令交互和自动推送
- ⏰ **定时任务** - 支持自定义时间的每日推送
- 📈 **技术指标** - SMA、RSI 等技术指标计算
- 💡 **投资建议** - 基于 AI 分析的买入/持有/卖出建议

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# DeepSeek API 配置
DEEPSEEK_API_KEY=your_deepseek_api_key

# Telegram Bot 配置
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# 股票列表（逗号分隔）
# A股: 上交所 .SS，深交所 .SZ
# 港股: .HK
STOCK_WATCH_LIST=600519.SS,601318.SS,0700.HK,000858.SZ

# 定时推送时间 (A股开盘 09:30，收盘 15:00)
SCHEDULE_TIMES=09:25,15:30

# 时区
TIMEZONE=Asia/Shanghai
```

### 3. 获取配置信息

#### DeepSeek API Key
1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册/登录账号
3. 在 API Keys 页面创建新的 API Key

#### Telegram Bot Token
1. 在 Telegram 搜索 `@BotFather`
2. 发送 `/newbot` 创建新机器人
3. 按照提示设置名称和用户名
4. 复制获取的 Bot Token

#### Telegram Chat ID
1. 在 Telegram 搜索 `@userinfobot`
2. 发送任意消息获取你的 Chat ID
3. 或者访问 `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` 获取

### 4. 运行程序

```bash
python main.py
```

## 使用方法

### Telegram Bot 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `/start` | 启动 Bot | /start |
| `/help` | 获取帮助 | /help |
| `/stock <代码>` | 查询股票 | /stock AAPL |
| `/analyze <代码>` | AI 分析 | /analyze 600519.SS |
| `/subscribe` | 订阅推送 | /subscribe |
| `/unsubscribe` | 取消订阅 | /unsubscribe |
| `/status` | 查看状态 | /status |

### 支持的股票代码

- **A股-上交所**: 加 `.SS`，如 `600519.SS` (贵州茅台)
- **A股-深交所**: 加 `.SZ`，如 `000858.SZ` (五粮液)
- **港股**: 加 `.HK`，如 `0700.HK` (腾讯控股)
- **美股**: 直接输入代码，如 `AAPL`

## 项目结构

```
stock-ai-agent/
├── config.py              # 配置文件
├── main.py                # 主程序入口
├── agents/
│   └── stock_agent.py     # 股票分析 Agent
├── services/
│   ├── stock_service.py    # 股票数据服务
│   ├── ai_service.py       # DeepSeek AI 服务
│   └── telegram_service.py # Telegram 服务
├── scheduler/
│   └── job_scheduler.py    # 定时任务调度器
├── utils/
│   └── logger.py           # 日志工具
├── requirements.txt        # 依赖列表
└── README.md               # 项目说明
```

## 配置说明

### 定时任务配置

```env
# 多个时间用逗号分隔
SCHEDULE_TIMES=09:25,15:30,20:00
```

### 关注股票列表

```env
# 逗号分隔的股票代码
# A股示例
STOCK_WATCH_LIST=600519.SS,601318.SS,000858.SZ
# 港股示例
STOCK_WATCH_LIST=0700.HK,9988.HK,3690.HK
```

### AI 模型参数

```env
AI_MODEL=deepseek-chat
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=1000
```

## 示例输出

### 股票查询
```
📈 AAPL - Apple Inc.

💰 价格: ¥189.45
+¥2.35 (+1.26%)

📊 基本信息:
• 开盘: ¥187.20
• 最高: ¥190.15
• 最低: ¥186.80
• 成交量: 45,234,100
• 52周最高: ¥199.62
• 52周最低: ¥124.17
• 市盈率(PE): 31.45
• 市值: ¥2.95万亿
```

### AI 分析报告
```
📊 600519.SS AI 分析报告

📈 贵州茅台

💰 价格: ¥189.45
+¥2.35 (+1.26%)

📉 技术指标:
• 5日均线: ¥187.20
• 10日均线: ¥185.50
• RSI(14): 58.4
• 趋势: 上升

🤖 AI 分析结论:
茅台近期表现强劲，业绩稳定...

💡 建议: 持有为主，可考虑在¥185附近适量加仓
```

## 注意事项

1. **API 限制**: 请注意 DeepSeek API 的调用频率限制
2. **市场时间**: 股票数据在非交易时间可能不更新
3. **投资风险**: AI 分析仅供参考，不构成投资建议
4. **网络要求**: 需要稳定的网络连接

## 故障排除

### 无法获取股票数据
- 检查股票代码是否正确
- 确认网络连接正常
- 可能是 Yahoo Finance 临时不可用

### Telegram 消息发送失败
- 确认 Bot Token 正确
- 确认 Chat ID 正确
- 确认 Bot 已启动并有发送消息权限

### AI 分析失败
- 检查 DeepSeek API Key 是否正确
- 检查 API 配额是否充足
- 查看日志获取详细错误信息

## 许可证

MIT License

## 作者

Stock AI Agent Team

## 版本

v1.0.0
