import os
import logging
from telethon import TelegramClient
import asyncio
from dotenv import load_dotenv

# 初始化日志
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# 加载 .env 文件中的环境变量
load_dotenv()


def load_config():
    """从环境变量加载API相关参数"""
    api_id = int(os.getenv('API_ID'))
    api_hash = os.getenv('API_HASH')
    bot_token = os.getenv('BOT_TOKEN')
    return api_id, api_hash, bot_token


def create_telegram_client(api_id, api_hash, bot_token):
    """创建并初始化Telegram客户端"""
    client = TelegramClient('bot', api_id, api_hash)
    client.start(bot_token=bot_token)
    return client


async def delete_files(client, channel_id):
    """删除指定频道中所有消息"""
    async for message in client.iter_messages(channel_id, limit=None):
        try:
            logging.info(f'Deleting message {message.id}')
            await message.delete()
        except Exception as e:
            logging.error(f'Failed to delete message {message.id}: {e}')


async def main():
    """程序主入口，执行删除操作"""
    api_id, api_hash, bot_token = load_config()
    client = create_telegram_client(api_id, api_hash, bot_token)
    channel_id = os.getenv('CHANNEL_ID')  # 从环境变量中获取频道ID
    await delete_files(client, channel_id)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f'An error occurred during the operation: {e}')
