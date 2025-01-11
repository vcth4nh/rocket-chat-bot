from rocketchat_async import RocketChat
from .methods import *

class BetterRocketChat(RocketChat):
    async def send_message(self, text, channel_id, thread_id=None):
        """Send a text message to a channel."""
        sent_msg_id = await SendMessage.call(self._dispatcher, text, channel_id, thread_id)
        return sent_msg_id

    async def update_message(self, text, orig_msg_id ,channel_id, thread_id=None):
        """Update a sent text message"""
        await UpdateMessage.call(self._dispatcher, text, orig_msg_id, channel_id, thread_id)

    async def send_typing_event(self, is_typing, channel_id, thread_id=None):
        """Send the `typing` event to a channel."""
        await SendTypingEvent.call(self._dispatcher, is_typing, channel_id, self.username, thread_id)
