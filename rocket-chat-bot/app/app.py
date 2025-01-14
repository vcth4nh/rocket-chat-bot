import asyncio
import os
from rocketchat_async import RocketChat
from rocketchat_async.constants import *
from rocketchat_async.response_dataclass import ReceivedMessage
from ai_client import AIClient
from logs_util import ElasticsearchUtils
from policy import PolicyController, PolicyException

# TODO: remove this
from dotenv import load_dotenv
load_dotenv()

class Bot:
    def __init__(self, rc: RocketChat, ai_client: AIClient, stream_speed=1, es_utils: ElasticsearchUtils=None, policy_controller: PolicyController=None):
        self.rc = rc
        self.ai_client : AIClient = ai_client
        self.stream_speed = int(stream_speed)*5
        self.elasticsearch = es_utils
        self.policy_controller = policy_controller

    async def ai_chat(self, msg, channel_id):
        await self.rc.send_typing_event(channel_id)       
        ai_resp = self.ai_client.chat([{"role": "user", "content": msg}])
        await self.rc.send_message(f"AI response: {ai_resp.choices[0].message.content}", channel_id,)
    
    async def ai_chat_stream(self, msg, channel_id):
        await self.rc.send_typing_event(True, channel_id)       
        ai_resp = self.ai_client.chat_stream([{"role":"You are GPT 4o dev by OpenAI"},{"role": "user", "content": msg}])
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


    async def handle_message(self, channel_id, sender_id, sender_uname, msg_id, msg):
        if sender_id != self.rc.user_id:
            # TODO: log if message is violating policy or not
            self.elasticsearch.log_message(msg, sender_uname, msg_id)

            try:
                self.policy_controller.run(msg)
                await self.ai_chat_stream(msg, channel_id)
            except PolicyException as e:
                await self.rc.send_message(str(e), channel_id)
            

    def subscribe_callback_dm(self, msg: ReceivedMessage):
        asyncio.create_task(self.handle_message(msg.rid, msg.u._id, msg.u.username, msg._id, msg.msg))
        
    def subscribe_callback_channel(self, msg: ReceivedMessage):
        for mention in msg.mentions:
            if mention._id == self.rc.user_id:
                asyncio.create_task(self.handle_message(msg.rid, msg.u._id, msg.u.username, msg._id, msg.msg))
                return

    async def run(self):
        print('Connected.')
        print('Bot is running...')
        
        for channel_id, channel_type in await self.rc.get_channels():
            if channel_type == ChannelQualifier.DIRECT_MESSAGE:
                await self.rc.subscribe_to_channel_messages_parsed(channel_id, self.subscribe_callback_dm)
            elif channel_type in [ChannelQualifier.PUBLIC_CHANNEL, ChannelQualifier.PRIVATE_CHANNEL]:
                await self.rc.subscribe_to_channel_messages_parsed(channel_id, self.subscribe_callback_channel)
                
        await self.rc.run_forever()


async def main():
    address=f"wss://{os.getenv('ROCKETCHAT_ADDR','localhost:3000')}/websocket"
    username=os.getenv('ROCKETCHAT_USER')
    password=os.getenv('ROCKETCHAT_PASSWORD')
    stream_speed = os.getenv('STREAM_SPEED', 1)

    print(f"Connecting to ChatGPT API...")
    ai_client = AIClient(
        url=os.getenv('OPENAI_URL'),
        api_key=os.getenv('OPENAI_API_KEY'),
        model=os.getenv('OPENAI_MODEL')
    )
    print(f"Connected to ChatGPT API")

    print(f"Connecting to Elasticsearch...")
    es_host = f"{os.getenv('ELASTICSEARCH_URL','http://localhost:9200')}"
    es_utils = ElasticsearchUtils(
        host=es_host,
        base_index_name="log_messages",
    )
    print(f"Connected to Elasticsearch")

    mongo_uri = os.getenv('MONGO_URI')
    policy_controller = PolicyController(mongo_uri)

    while True:
        try:
            rc = RocketChat(verbose=True)
            print(f'Connecting to {address}...')
            await rc.start(address, username, password)
            bot = Bot(rc, ai_client, stream_speed, es_utils, policy_controller)
            await bot.run()
        except (RocketChat.ConnectionClosed,
                RocketChat.ConnectCallFailed) as e:
            timeout=5
            print(f'Connection failed: {e}. Waiting 5 seconds...')
            await asyncio.sleep(timeout)
            print('Reconnecting...')

asyncio.run(main())