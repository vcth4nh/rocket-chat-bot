import asyncio
import random
import os
from better_rocketchat_async import BetterRocketChat 
from pprint import pprint
import asyncio
import random
from AIClient import AIClient

class Bot:
    def __init__(self, rc: BetterRocketChat, ai_client: AIClient, stream_speed=1):
        self.rc = rc
        self.ai_client : AIClient = ai_client
        self.stream_speed = int(stream_speed)*5

    async def ai_chat(self, msg, channel_id):
        await self.rc.send_typing_event(channel_id)       
        ai_resp = self.ai_client.chat([{"role": "user", "content": msg}])
        await self.rc.send_message(f"AI response: {ai_resp.choices[0].message.content}", channel_id,)
    
    async def ai_chat_stream(self, msg, channel_id):
        await self.rc.send_typing_event(True, channel_id)       
        ai_resp = self.ai_client.chat_stream([{"role": "user", "content": msg}])
        await self.rc.send_typing_event(False, channel_id)

        first = True
        sent_msg_id = None
        ai_full_resp = ""
        ai_full_resp_buffer = ""
        for chunk in ai_resp:
            if len(ai_full_resp_buffer) > self.stream_speed:
                ai_full_resp += ai_full_resp_buffer
                ai_full_resp_buffer = ""
            else:
                ai_full_resp_buffer += chunk.choices[0].delta.content or ""
                continue

            if first:
                sent_msg_id = await self.rc.send_message(ai_full_resp, channel_id)
                first = False
                continue
        
            await self.rc.update_message(ai_full_resp, sent_msg_id, channel_id)
        
        if ai_full_resp_buffer:
            ai_full_resp += ai_full_resp_buffer
            await self.rc.update_message(ai_full_resp, sent_msg_id, channel_id)


    async def handle_message(self, channel_id, sender_id, msg_id, thread_id, msg, qualifier, unread, repeated):
        if sender_id != self.rc.user_id:
            await self.ai_chat_stream(msg, channel_id)

    def subscribe_callback(self, *args):
        asyncio.create_task(self.handle_message(*args))


    async def run(self):
        print('Connected.')
        print('Bot is running...')
        for channel_id, channel_type in await self.rc.get_channels():
            await self.rc.subscribe_to_channel_messages(channel_id, self.subscribe_callback)
        await self.rc.run_forever()


async def main():
    address=f"wss://{os.getenv('ROCKETCHAT_DOMAIN','localhost')}:{os.getenv('ROCKETCHAT_PORT',3000)}/websocket"
    print(f'Connecting to {address}...')
    username=os.getenv('ROCKETCHAT_USER')
    password=os.getenv('ROCKETCHAT_PASSWORD')
    stream_speed = os.getenv('STREAM_SPEED', 1)
    ai_client = AIClient(
        url=os.getenv('OPENAI_URL'),
        api_key=os.getenv('OPENAI_API'),
        model=os.getenv('OPENAI_MODEL')
    )
    while True:
        try:
            rc = BetterRocketChat()
            await rc.start(address, username, password)
            bot = Bot(rc, ai_client, stream_speed)
            await bot.run()
        except (BetterRocketChat.ConnectionClosed,
                BetterRocketChat.ConnectCallFailed) as e:
            print(f'Connection failed: {e}. Waiting a few seconds...')
            await asyncio.sleep(random.uniform(4, 8))
            print('Reconnecting...')

asyncio.run(main())