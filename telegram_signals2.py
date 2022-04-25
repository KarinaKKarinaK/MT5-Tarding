#Code from: https://stackoverflow.com/questions/61552973/getting-signals-from-telegram-channel-and-placing-them-in-mt4-using-python
import configparser
import json
import telegram

from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import PeerChannel
from telethon.tl.functions.messages import (GetHistoryRequest)


my_channel = "-1005056751438"



# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)


async def main():
    me = await client.get_me()
    print(me.stringify())
    async for message in client.iter_messages('GOLD KILLER'):
        print(message.id, message.text)

with client:
    client.loop.run_until_complete(main())

@client.on(events.NewMessage)
async def my_event_handler(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    chat_id = event.chat_id
    sender_id = event.sender.id
    text = event.raw_text
    # print(sender.id)
    if sender_id == 1386059246:
        print(event.raw_text)
client.start()
client.run_until_disconnected()