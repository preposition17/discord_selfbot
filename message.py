from datetime import datetime

from .api import Api

from .channel import Channel
from .guild import Guild
from .user import User


class Message:
    def __init__(self, message_data: dict, api: Api):
        """
        Discord message object
        :param message_data: message data from Discord Api or discord_selfbot.SelfBot
        :param api: discord_selfbot.Api
        """
        self.api = api

        self._message_data = message_data
        self.time = datetime.fromisoformat(self._message_data["timestamp"])
        self.content = self._message_data["content"]

        if self._message_data["attachments"]:
            self.attachments = [attachment["url"] for attachment in self._message_data["attachments"]]

        self.author = User(self._message_data["author"])

        self._guild = None
        self._channel = None

    @property
    def raw(self):
        return self._message_data

    @property
    def channel_id(self):
        return self._message_data["channel_id"]

    @property
    def guild_id(self):
        return self._message_data["guild_id"]

    @property
    def channel(self) -> Channel:
        """
        Get Channel instance of message
        :return: discord_selfbot.Channel instance
        """
        if not self._channel:
            self._channel = self.api.get_channel(self._message_data["channel_id"])
        return self._channel

    @property
    def guild(self) -> Guild:
        """
        Get Guild instance of message
        :return: discord_selfbot.Guild instance
        """
        if not self._guild:
            self._guild = self.api.get_guild(self.channel.guild_id)
        return self._guild
