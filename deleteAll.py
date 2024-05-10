import os
import logging
from telethon import TelegramClient
import asyncio
import configparser

# 初始化日志
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def load_config():
    """加载配置文件，返回API相关参数"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_id = int(config['TELEGRAM']['API_ID'])
    api_hash = config['TELEGRAM']['API_HASH']
    bot_token = config['TELEGRAM']['BOT_TOKEN']
    return api_id, api_hash, bot_token


def create_telegram_client(api_id, api_hash, bot_token):
    """创建并初始化Telegram客户端"""
    client = TelegramClient('bot', api_id, api_hash)
    client.start(bot_token=bot_token)
    return client


async def delete_files(client, channel_id):
    """删除指定频道中所有带有文件的消息"""
    async for message in client.iter_messages(channel_id, limit=None):
        if message.file:
            try:
                logging.info(f'Deleting message {message.id} with file {message.file.name}')
                await message.delete()
            except Exception as e:
                logging.error(f'Failed to delete message {message.id}: {e}')
                continue


async def main():
    """程序主入口，执行删除操作"""
    api_id, api_hash, bot_token = load_config()
    client = create_telegram_client(api_id, api_hash, bot_token)
    channel_id = 'your_channel_id'  # 应从安全来源获取
    await delete_files(client, channel_id)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f'An error occurred during the operation: {e}')
