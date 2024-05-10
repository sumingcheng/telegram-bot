from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, CallbackContext
import os


def start(update: Update, context: CallbackContext) -> None:
  update.message.reply_text('欢迎使用本机器人！发送 /sendfiles 命令来上传文件夹中的所有文件到指定频道。')


def send_files(update: Update, context: CallbackContext) -> None:
  # 指定文件夹路径
  folder_path = 'path/to/your/folder'
  # 指定频道ID或用户名
  channel_id = '@your_channel_name'

  # 遍历文件夹中的所有文件
  for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
      try:
        # 读取文件并发送到频道
        document = InputFile(file_path)
        caption = f'文件名: {filename}'
        context.bot.send_document(chat_id=channel_id, document=document, caption=caption)
        update.message.reply_text(f'文件 {filename} 已成功上传到频道。')
      except Exception as e:
        update.message.reply_text(f'发送文件 {filename} 时出现错误。')
        print(f"Error: {e}")


def main() -> None:
  # 替换'TOKEN'为你的机器人的Token
  updater = Updater("TOKEN", use_context=True)

  dp = updater.dispatcher
  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("sendfiles", send_files))

  # 启动机器人
  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()
