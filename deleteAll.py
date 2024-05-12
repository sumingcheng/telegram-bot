import os
import logging
from telethon import TelegramClient
import asyncio
from dotenv import load_dotenv
import python_socks

# 设置日志配置
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('TelegramDeleter')

# 加载环境变量
load_dotenv()


def check_env_vars(*vars):
    """检查必要的环境变量是否已设置，如果缺少变量，则抛出错误。"""
    missing_vars = [var for var in vars if not os.getenv(var)]
    if missing_vars:
        error_message = f"缺少必要的环境变量：{', '.join(missing_vars)}"
        logger.error(error_message)
        raise ValueError(error_message)


def load_config():
    """从环境变量加载配置，返回API ID、API Hash、频道 ID 和代理 URL。"""
    check_env_vars('API_ID', 'API_HASH', 'CHANNEL_ID')  # 检查环境变量
    api_id = int(os.getenv('API_ID'))
    api_hash = os.getenv('API_HASH')
    channel_id = int(os.getenv('CHANNEL_ID'))
    proxy_url = os.getenv('PROXY_URL', 'http://localhost:7890')
    return api_id, api_hash, channel_id, proxy_url


async def create_telegram_client(api_id, api_hash, proxy_url):
    """创建并返回一个连接的 Telegram 客户端，包括代理设置。"""
    proxy_type, host, port, username, password = python_socks.parse_proxy_url(proxy_url)
    client = TelegramClient('session', api_id, api_hash, proxy=(proxy_type, host, port, username, password))
    await client.start()
    logger.info("Telegram 客户端已成功连接。")
    return client


async def delete_all_messages(client, channel_id):
    """异步删除指定频道中的所有消息。"""
    entity = await client.get_entity(channel_id)
    async for message in client.iter_messages(entity):
        try:
            await message.delete()
            logger.info(f'消息ID {message.id} 已删除。')
        except Exception as e:
            logger.error(f'删除消息ID {message.id} 失败：{e}')


async def main():
    """主函数，执行消息删除流程。"""
    api_id, api_hash, channel_id, proxy_url = load_config()
    client = await create_telegram_client(api_id, api_hash, proxy_url)
    try:
        await delete_all_messages(client, channel_id)
    finally:
        await client.disconnect()
        logger.info("Telegram 客户端已断开连接。")


if __name__ == '__main__':
    asyncio.run(main())
