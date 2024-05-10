from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, CallbackContext
import os


def start(update: Update, context: CallbackContext) -> None:
  update.message.reply_text('欢迎使用本机器人！发送 /sendfiles 命令来上传文件夹中的所有文件到指定频道。')


def send_files(update: Update, context: CallbackContext) -> None:
  folder_path = 'path/to/your/folder'
  channel_id = '@your_channel_name'

  for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
      try:
        document = InputFile(file_path)
        caption = f'文件名: {filename}'
        context.bot.send_document(chat_id=channel_id, document=document, caption=caption)
        update.message.reply_text(f'文件 {filename} 已成功上传到频道。')
      except Exception as e:
        update.message.reply_text(f'发送文件 {filename} 时出现错误。')
        print(f"Error: {e}")


def delete_files(update: Update, context: CallbackContext) -> None:
  channel_id = '@your_channel_name'
  bot = context.bot
  try:
    for message in bot.iter_chat_messages(channel_id):
      if message.document:
        bot.delete_message(chat_id=channel_id, message_id=message.message_id)
    update.message.reply_text('频道中的所有文件已被删除。')
  except Exception as e:
    update.message.reply_text('删除文件时出现错误。')
    print(f"Error: {e}")


def main() -> None:
  updater = Updater("TOKEN", use_context=True)

  dp = updater.dispatcher
  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("sendfiles", send_files))
  dp.add_handler(CommandHandler("deletefiles", delete_files))

  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()
