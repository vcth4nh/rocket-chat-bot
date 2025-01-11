import asyncio
import random
import os
from rocketchat_async import RocketChat as RocketChatAsync
from rocketchat_API.rocketchat import RocketChat
from dotenv import load_dotenv
from pprint import pprint
from logs_util import ElasticsearchUtils
import json

load_dotenv()

class Bot:
    def __init__(self, rc_async: RocketChatAsync, rc: RocketChat, es_utils: ElasticsearchUtils):
        self.rc_async = rc_async
        self.rc = rc
        self.es = es_utils
    
    async def get_username_from_id(self, user_id):
        try:
            # Use the RocketChat users.info endpoint to fetch user details
            response = self.rc.users_info(user_id=user_id)
            users = response.content
            user_info = json.loads(users)
            return user_info.get("user", {}).get("username", "unknown")
        except Exception as e:
            print(f"Error fetching username for user_id {user_id}: {e}")
            return 'unknown'

    async def handle_message(self, channel_id, sender_id, msg_id, thread_id, msg, qualifier, unread, repeated):
        if sender_id != self.rc_async.user_id:
            sender_username = await self.get_username_from_id(sender_id)
            
            self.es.log_message(msg, sender_username, msg_id)
            
            await self.rc_async.send_message(f"{msg} cc", channel_id)

    def subscribe_callback(self, *args):
        pprint(args)
        asyncio.create_task(self.handle_message(*args))

    async def run(self):
        print('Connected.')
        print('Bot is running...')
        for channel_id, channel_type in await self.rc_async.get_channels():
            await self.rc_async.subscribe_to_channel_messages(channel_id,
                                                        self.subscribe_callback)
        await self.rc_async.run_forever()


async def main():
    async_address=f"wss://{os.getenv('ROCKETCHAT_DOMAIN','localhost')}:{os.getenv('ROCKETCHAT_PORT',3000)}/websocket"
    address = f"https://{os.getenv('ROCKETCHAT_DOMAIN', 'localhost')}"

    print(f'Connecting to {address}...')
    username=os.getenv('ROCKETCHAT_USER')
    password=os.getenv('ROCKETCHAT_PASSWORD')

    es_host = f"{os.getenv('ELASTICSEARCH_HOST','http://localhost')}:{os.getenv('ELASTICSEARCH_PORT',9200)}"
    es_utils = ElasticsearchUtils(
        host=es_host,
        base_index_name="log_messages",
    )

    rc = RocketChat(username, password, server_url=address)

    while True:
        try:
            rc_async = RocketChatAsync()
            await rc_async.start(async_address, username, password)
            bot = Bot(rc_async, rc, es_utils)
            await bot.run()
        except (RocketChatAsync.ConnectionClosed,
                RocketChatAsync.ConnectCallFailed) as e:
            print(f'Connection failed: {e}. Waiting a few seconds...')
            await asyncio.sleep(random.uniform(4, 8))
            print('Reconnecting...')

asyncio.run(main())