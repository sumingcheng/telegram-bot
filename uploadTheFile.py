from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
import logging
from dotenv import load_dotenv

# 配置日志记录
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 从环境变量中获取配置
FOLDER_PATH = os.getenv('FOLDER_PATH')
CHANNEL_ID = os.getenv('CHANNEL_ID')
TOKEN = os.getenv('TOKEN')

# 检查环境变量是否已正确设置
if not all([FOLDER_PATH, CHANNEL_ID, TOKEN]):
    logger.error("请确保.env文件中包含FOLDER_PATH, CHANNEL_ID, 和 TOKEN")
    exit(1)


def start(update: Update, context: CallbackContext) -> None:
    """处理/start命令，发送欢迎信息。"""
    update.message.reply_text('😀欢迎使用本机器人！发送 / 可以获取更多命令。')
    logger.info(f"User {update.effective_user.id} started the bot.")


def send_files(update: Update, context: CallbackContext) -> None:
    """遍历指定文件夹并发送文件到频道。"""
    try:
        for filename in os.listdir(FOLDER_PATH):
            file_path = os.path.join(FOLDER_PATH, filename)
            if os.path.isfile(file_path):
                send_file_to_channel(file_path, filename, context, update)
    except Exception as e:
        logger.error(f"读取文件夹时出现错误: {e}")
        update.message.reply_text('读取文件夹时出现错误。')


def send_file_to_channel(file_path: str, filename: str, context, update):
    """发送单个文件到频道。"""
    try:
        with open(file_path, 'rb') as file:
            document = InputFile(file)
            caption = f'文件名: {filename}'
            context.bot.send_document(chat_id=CHANNEL_ID, document=document, caption=caption)
        update.message.reply_text(f'文件 {filename} 已成功上传到频道。')
        logger.info(f"File {filename} sent successfully to channel {CHANNEL_ID}.")
    except Exception as e:
        logger.error(f"发送文件 {filename} 时出现错误: {e}")
        update.message.reply_text(f'发送文件 {filename} 时出现错误。')


def main() -> None:
    """主函数，配置并启动 Telegram bot。"""
    logger.info("Starting bot...")
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
