import telegram
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import os
import logging
from dotenv import load_dotenv

# 配置日志记录
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 从环境变量中获取配置
CHANNEL_ID = os.getenv('CHANNEL_ID')
TOKEN = os.getenv('TOKEN')

# 检查环境变量是否已正确设置
if not all([CHANNEL_ID, TOKEN]):
    logger.error("确保.env文件中包含了CHANNEL_ID和TOKEN")
    exit(1)


def start(update: Update, context: CallbackContext) -> None:
    """处理/start命令，发送欢迎信息。"""
    update.message.reply_text('😀欢迎使用本机器人！请上传文件。')
    logger.info(f"用户 {update.effective_user.id} 启动了机器人。")


def handle_document(update: Update, context: CallbackContext) -> None:
    """处理用户上传的文件，发送文件名到频道。"""
    document = update.message.document
    file = context.bot.get_file(document.file_id)
    filename = document.file_name

    try:
        # 发送文件名到指定频道
        context.bot.send_message(chat_id=CHANNEL_ID, text=f'{filename} 文件上传成功。')
        logger.info(f"文件 {filename} 成功上传并发送通知到频道 {CHANNEL_ID}。")
    except Exception as e:
        logger.error(f"发送文件 {filename} 上传成功通知时出错: {e}")
        update.message.reply_text(f'发送文件上传成功通知时出错。')


def main() -> None:
    """主函数，配置并启动 Telegram bot。"""
    logger.info("机器人启动中...")
    # 代理配置
    request_kwargs = {
        'proxy_url': 'http://127.0.0.1:7890',  # 示例代理地址
        'connect_timeout': 10,
        'read_timeout': 30
    }
    updater = Updater(TOKEN, use_context=True, request_kwargs=request_kwargs)
    dp = updater.dispatcher

    # 命令处理
    dp.add_handler(CommandHandler("start", start))
    # 文件上传处理
    dp.add_handler(MessageHandler(Filters.document, handle_document))

    updater.start_polling()
    logger.info("机器人已启动并开始轮询。")
    updater.idle()
    logger.info("机器人已停止。")


if __name__ == '__main__':
    main()
