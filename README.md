# Telegram Bot 功能集

本项目包含一个 Telegram 机器人的几个核心功能实现，涵盖删除消息、上传文件和代理测试。这些功能利用 Python 和 Telegram API 实现，主要包括以下文件：

- `deleteAll.py`：删除指定 Telegram 频道中的所有消息。
- `uploadTheFile.py`：将文件上传到指定的 Telegram 频道。
- `proxyTesting.py`：测试代理服务器的连通性及性能。

## 功能说明

### 1. 删除所有消息（`deleteAll.py`）

脚本通过 Telegram API 删除一个指定频道中的所有消息，依赖 `telethon` 库实现消息的批量删除。

### 2. 上传文件（`uploadTheFile.py`）

脚本使用 `python-telegram-bot` 库从本地上传文件到指定的 Telegram 频道，支持多种文件格式。

### 3. 代理测试（`proxyTesting.py`）

脚本用于验证代理服务器的设置，确保机器人能在特定网络环境下正常连接到 Telegram 服务器。

## 安装与配置

1. **安装依赖：** 使用以下命令安装所需的库：

   ```
   bash
   Copy code
   pip install telethon python-telegram-bot
   ```

2. **设置环境变量：** 在 `.env` 文件中配置必要的环境变量：

   - `API_ID`: Telegram API ID。
   - `API_HASH`: Telegram API Hash。
   - `BOT_TOKEN`: Telegram 机器人 Token。
   - `CHANNEL_ID`: 目标 Telegram 频道 ID。

3. **运行脚本：** 通过 Python 直接运行相应的脚本文件。

   ```
   bashCopy codepython deleteAll.py
   python uploadTheFile.py
   python proxyTesting.py
   ```

## 注意事项

- 确保机器人具备在指定频道进行消息发送和删除的权限。
- 代理测试需配置正确的代理地址和端口，并确保该代理可访问 Telegram。

这些脚本为开发者提供了操作 Telegram 机器人的基础模板，可根据具体需求进行修改和扩展。
