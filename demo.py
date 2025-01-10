import asyncio
import random
import os
from rocketchat_async import RocketChat
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


import asyncio
import random
from rocketchat_async import RocketChat

class Bot:
    def __init__(self, rc: RocketChat):
        self.rc = rc
    
    async def handle_message(self, channel_id, sender_id, msg_id, thread_id, msg, qualifier, unread, repeated):
        if sender_id != self.rc.user_id:
            await self.rc.send_message(f"{msg} cc", channel_id)

    def subscribe_callback(self, *args):
        pprint(args)
        asyncio.create_task(self.handle_message(*args))


    async def run(self):
        print('Connected.')
        print('Bot is running...')
        for channel_id, channel_type in await self.rc.get_channels():
            await self.rc.subscribe_to_channel_messages(channel_id,
                                                        self.subscribe_callback)
        await self.rc.run_forever()


async def main():
    address=f"wss://{os.getenv('ROCKETCHAT_DOMAIN','localhost')}:{os.getenv('ROCKETCHAT_PORT',3000)}/websocket"
    print(f'Connecting to {address}...')
    username=os.getenv('ROCKETCHAT_USER')
    password=os.getenv('ROCKETCHAT_PASSWORD')
    while True:
        try:
            rc = RocketChat()
            await rc.start(address, username, password)
            bot = Bot(rc)
            await bot.run()
        except (RocketChat.ConnectionClosed,
                RocketChat.ConnectCallFailed) as e:
            print(f'Connection failed: {e}. Waiting a few seconds...')
            await asyncio.sleep(random.uniform(4, 8))
            print('Reconnecting...')

asyncio.run(main())