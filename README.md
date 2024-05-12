# Telegram Bot 功能集 🤖

本项目包含一个 Telegram 机器人的核心功能实现，涉及删除消息、上传文件和代理测试。以下表格详细描述了各个功能的实现文件和说明：

| 文件名             | 功能描述                                                     |
| ------------------ | ------------------------------------------------------------ |
| `deleteAll.py`     | 删除指定 Telegram 频道中的所有消息。                         |
| `uploadTheFile.py` | 将文件上传到指定的 Telegram 频道。                           |
| `proxyTesting.py`  | 测试代理服务器的连通性及性能，确保机器人能在特定网络环境下正常工作。 |

## 安装与配置 🛠️

### 安装依赖

使用以下命令安装所需的库：

```
bash
Copy code
pip install telethon python-telegram-bot
```

### 设置环境变量

在 `.env` 文件中配置必要的环境变量：

| 环境变量     | 说明                    |
| ------------ | ----------------------- |
| `API_ID`     | Telegram API ID。       |
| `API_HASH`   | Telegram API Hash。     |
| `BOT_TOKEN`  | Telegram 机器人 Token。 |
| `CHANNEL_ID` | 目标 Telegram 频道 ID。 |

### 运行脚本

通过 Python 直接运行相应的脚本文件：

```
bashCopy codepython deleteAll.py
python uploadTheFile.py
python proxyTesting.py
```

## 注意事项 🔍

- 确保机器人具备在指定频道进行消息发送和删除的权限。
- 代理测试需配置正确的代理地址和端口，并确保该代理可访问 Telegram。

本项目的脚本为开发者提供了操作 Telegram 机器人的基础模板，可根据具体需求进行修改和扩展。
