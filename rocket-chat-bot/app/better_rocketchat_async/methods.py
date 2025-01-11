import hashlib
import time
from rocketchat_async.methods import RealtimeRequest
class UpdateMessage(RealtimeRequest):
    """Update a sent message"""

    @staticmethod
    def _get_request_msg(msg_id, orig_msg_id, channel_id, msg_text, thread_id=None):
        msg = {
            "msg": "method",
            "method": "updateMessage",
            "id": msg_id,
            "params": [
                {
                    "_id": orig_msg_id,
                    "rid": channel_id,
                    "msg": msg_text
                }
            ]
        }
        if thread_id is not None:
            msg["params"][0]["tmid"] = thread_id
        return msg

    @classmethod
    async def call(cls, dispatcher, msg_text, orig_msg_id, channel_id, thread_id=None):
        msg_id = cls._get_new_id()
        msg = cls._get_request_msg(msg_id, orig_msg_id, channel_id, msg_text, thread_id)
        # print(msg)
        await dispatcher.call_method(msg, msg_id)

class SendMessage(RealtimeRequest):
    """Send a text message to a channel."""

    @staticmethod
    def _get_request_msg(msg_id, channel_id, msg_text, thread_id=None):
        id_seed = f'{msg_id}:{time.time()}'
        msg = {
            "msg": "method",
            "method": "sendMessage",
            "id": msg_id,
            "params": [
                {
                    "_id": hashlib.md5(id_seed.encode()).hexdigest()[:12],
                    "rid": channel_id,
                    "msg": msg_text
                }
            ]
        }
        if thread_id is not None:
            msg["params"][0]["tmid"] = thread_id
        return msg

    @classmethod
    async def call(cls, dispatcher, msg_text, channel_id, thread_id=None):
        msg_id = cls._get_new_id()
        msg = cls._get_request_msg(msg_id, channel_id, msg_text, thread_id)
        # print(msg)
        await dispatcher.call_method(msg, msg_id)
        return msg["params"][0]["_id"]

class SendTypingEvent(RealtimeRequest):
    """Send the `typing` event to a channel."""

    @staticmethod
    def _get_request_msg(msg_id, is_typing, channel_id, username, thread_id=None):
        msg = {
            "msg": "method",
            "method": "stream-notify-room",
            "id": msg_id,
            "params": [
                f'{channel_id}/typing',
                username,
                is_typing
            ]
        }
        if(thread_id):
            msg["params"][-1]["tmid"] = thread_id
        return msg

    @classmethod
    async def call(cls, dispatcher, is_typing, channel_id, username, thread_id=None):
        msg_id = cls._get_new_id()
        is_typing = bool(is_typing)
        msg = cls._get_request_msg(msg_id, is_typing, channel_id, username, thread_id)
        # print(msg)
        await dispatcher.call_method(msg, msg_id)
