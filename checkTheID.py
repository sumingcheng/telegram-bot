from telethon.sync import TelegramClient

# 用您的api_id和api_hash替换下面的值
api_id = 'your_api_id'
api_hash = 'your_api_hash'
phone_number = 'your_phone_number'  # 用您的电话号码替换

client = TelegramClient('anon', api_id, api_hash)


async def main():
  # 这里可以选择按名称或者是您知道的部分信息查找
  async for dialog in client.iter_dialogs():
    print(dialog.name, 'has ID:', dialog.id)


with client:
  client.start(phone=phone_number)  # 第一次会要求您输入验证码
  client.loop.run_until_complete(main())


# 可以直接拉 getmyid_bot 机器人查看