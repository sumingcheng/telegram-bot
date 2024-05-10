from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
import logging
from dotenv import load_dotenv

# 设置日志记录
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 加载.env文件
load_dotenv()

# 从环境变量中获取必要的配置
FOLDER_PATH = os.getenv('FOLDER_PATH')
CHANNEL_ID = os.getenv('CHANNEL_ID')
TOKEN = os.getenv('TOKEN')

if not all([FOLDER_PATH, CHANNEL_ID, TOKEN]):
  logging.error("请确保.env文件中包含FOLDER_PATH, CHANNEL_ID, 和 TOKEN")
  exit(1)


def start(update: Update, context: CallbackContext) -> None:
  update.message.reply_text('欢迎使用本机器人！发送 /sendfiles 命令来上传文件夹中的所有文件到指定频道。')


def send_files(update: Update, context: CallbackContext) -> None:
  try:
    for filename in os.listdir(FOLDER_PATH):
      file_path = os.path.join(FOLDER_PATH, filename)
      if os.path.isfile(file_path):
        send_file_to_channel(file_path, filename, context, update)
  except Exception as e:
    update.message.reply_text('读取文件夹时出现错误。')
    logging.error(f"Error reading the folder: {e}")


def send_file_to_channel(file_path: str, filename: str, context: CallbackContext, update: Update) -> None:
  try:
    document = InputFile(file_path)
    caption = f'文件名: {filename}'
    context.bot.send_document(chat_id=CHANNEL_ID, document=document, caption=caption)
    update.message.reply_text(f'文件 {filename} 已成功上传到频道。')
  except Exception as e:
    update.message.reply_text(f'发送文件 {filename} 时出现错误。')
    logging.error(f"Error sending file {filename}: {e}")


def delete_files(update: Update, context: CallbackContext) -> None:
  bot = context.bot
  try:
    for message in bot.iter_chat_messages(CHANNEL_ID):
      if message.document:
        bot.delete_message(chat_id=CHANNEL_ID, message_id=message.message_id)
    update.message.reply_text('频道中的所有文件已被删除。')
  except Exception as e:
    update.message.reply_text('删除文件时出现错误。')
    logging.error(f"Error deleting files: {e}")


def main() -> None:
  updater = Updater(TOKEN, use_context=True)
  dp = updater.dispatcher
  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("sendfiles", send_files))
  dp.add_handler(CommandHandler("deletefiles", delete_files))

  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()
