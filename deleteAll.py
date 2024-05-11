import os
import logging
from telethon import TelegramClient, errors
import asyncio
from dotenv import load_dotenv
import socks

# 初始化日志
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# 加载 .env 文件中的环境变量
load_dotenv()


def check_env_vars(*vars):
    """检查必要的环境变量是否已设置"""
    missing_vars = [var for var in vars if not os.getenv(var)]
    if missing_vars:
        error_message = f"环境变量设置不完整，请检查以下变量是否已配置: {', '.join(missing_vars)}"
        logging.error(error_message)
        raise ValueError(error_message)


def load_config():
    """从环境变量加载API相关参数"""
    api_id = int(os.getenv('API_ID'))
    api_hash = os.getenv('API_HASH')
    bot_token = os.getenv('BOT_TOKEN')
    channel_id = os.getenv('CHANNEL_ID')
    proxy_host = os.getenv('PROXY_HOST', 'localhost')
    proxy_port = int(os.getenv('PROXY_PORT', 1080))  # 假设你的 SOCKS5 代理端口为 1080
    return api_id, api_hash, bot_token, channel_id, proxy_host, proxy_port


async def create_telegram_client(api_id, api_hash, bot_token, proxy_host, proxy_port):
    proxy = (socks.SOCKS5, proxy_host, proxy_port)
    client = TelegramClient('bot', api_id, api_hash, proxy=proxy)
    try:
        await client.start(bot_token=bot_token)
        logging.info("Telegram 客户端成功连接。")
    except Exception as e:
        logging.error(f"启动 Telegram 客户端时出错: {e}")
        raise
    return client


async def delete_files(client, channel_id):
    """删除指定频道中所有消息"""
    async for message in client.iter_messages(channel_id, limit=None):
        try:
            await message.delete()
            logging.info(f'消息 {message.id} 已删除')
        except Exception as e:
            logging.error(f'删除消息 {message.id} 失败: {e}')


async def main():
    """程序主入口，执行删除操作"""
    api_id, api_hash, bot_token, channel_id, proxy_host, proxy_port = load_config()
    client = await create_telegram_client(api_id, api_hash, bot_token, proxy_host, proxy_port)
    try:
        await delete_files(client, channel_id)
    finally:
        if client.is_connected():
            await client.disconnect()
            logging.info("Telegram 客户端已断开连接。")


if __name__ == '__main__':
    asyncio.run(main())
