import telegram
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
import logging
from dotenv import load_dotenv
import sqlite3

# 配置日志记录
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 从环境变量中获取配置
FOLDER_PATH = os.getenv('FOLDER_PATH')
CHANNEL_ID = os.getenv('CHANNEL_ID')
TOKEN = os.getenv('TOKEN')
DB_PATH = os.getenv('DB_PATH', 'uploaded_files.db')  # SQLite数据库文件路径


# 初始化数据库
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS uploaded_files (filename TEXT PRIMARY KEY)')
    conn.commit()
    conn.close()


# 检查文件是否已上传
def is_uploaded(filename):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT filename FROM uploaded_files WHERE filename = ?', (filename,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


# 保存已上传文件名到数据库
def save_uploaded_file(filename):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO uploaded_files (filename) VALUES (?)', (filename,))
    conn.commit()
    conn.close()


def start(update: Update, context: CallbackContext) -> None:
    """处理/start命令，发送欢迎信息。"""
    update.message.reply_text('😀欢迎使用本机器人！发送 /sendfiles 可以上传文件。')
    logger.info(f"User {update.effective_user.id} started the bot.")


def send_files(update: Update, context: CallbackContext) -> None:
    """遍历指定文件夹并发送文件到频道，并更新上传进度。"""
    files = os.listdir(FOLDER_PATH)
    total_files = len(files)
    uploaded_count = 0

    for filename in files:
        file_path = os.path.join(FOLDER_PATH, filename)
        if os.path.isfile(file_path) and not is_uploaded(filename):
            if send_file_to_channel(file_path, filename, context, update):
                uploaded_count += 1
                save_uploaded_file(filename)  # 保存已上传的文件名
            update.message.reply_text(f'已成功上传 {uploaded_count} / {total_files} 个文件。')


import time


def send_file_to_channel(file_path: str, filename: str, context, update):
    """发送单个文件到频道，并返回上传状态。"""
    try:
        with open(file_path, 'rb') as file:
            document = InputFile(file)
            caption = f'文件名: {filename}'
            context.bot.send_document(chat_id=CHANNEL_ID, document=document, caption=caption)
        logger.info(f"File {filename} sent successfully to channel {CHANNEL_ID}.")
        time.sleep(1)  # 简单示例，每次发送后暂停1秒
        return True
    except telegram.error.RetryAfter as e:
        logger.warning(f"Reached rate limit, need to wait {e.retry_after} seconds")
        time.sleep(e.retry_after)
        return send_file_to_channel(file_path, filename, context, update)  # 重试发送
    except Exception as e:
        logger.error(f"发送文件 {filename} 时出现错误: {e}")
        update.message.reply_text(f'发送文件 {filename} 时出现错误。')
        return False


def main() -> None:
    """主函数，配置并启动 Telegram bot。"""
    logger.info("Starting bot...")
    init_db()  # 初始化数据库
    request_kwargs = {
        'proxy_url': 'http://127.0.0.1:7890',  # 示例代理地址
        'connect_timeout': 10,
        'read_timeout': 30
    }
    updater = Updater(TOKEN, use_context=True, request_kwargs=request_kwargs)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sendfiles", send_files))

    updater.start_polling()
    logger.info("Bot started and polling initiated.")
    updater.idle()
    logger.info("Bot stopped.")


if __name__ == '__main__':
    main()
