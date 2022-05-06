from typing import Union, Text

from requests import Session
from requests import Response

from .config import Config

from .guild import Guild
from .channel import Channel
from .user import User


class Api(Session):
    def __init__(self, token, config: Config = None):
        """
        Api based on requests.Session for Discord
        Use { api = Api.init(token) }
        :param token: your discord user token
        :param config: discord_selfbot.Config
        """
        super().__init__()

        if config:
            self.config = config
        else:
            self.config = Config(token)

        self.api_url = config.api_url

        self.token = token
        self.bearer = None

    @classmethod
    def init(cls, token, config: Config = None):
        """
        :param token: your discord user token
        :param config: discord_selfbot.Config
        :return: discord_selfbot.Api
        """
        if not config:
            config = Config(token)
        api = cls(token, Config(token))

        api.headers.update({
            "user-agent": config.useragent,
            "authorization": token,
            "content-type": "application/json",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
        })
        return api

    def get(self, endpoint: str, **kwargs) -> dict:
        """
        Get request on Discord api
        :param endpoint: discord api endpoint, ex. "/guilds"
        :param kwargs: kwargs for requests.Session.get()
        :return: dict with data
        """
        return super().get(url=f"{self.api_url}{endpoint}", **kwargs).json()

    def post(self, endpoint: str, data=None, json=None, **kwargs) -> dict:
        """
        Post request on Discord api
        :param endpoint: discord api endpoint, ex. "/login"
        :param data: request.Session.post() data param
        :param json: request.Session.post() json param
        :param kwargs: kwargs for requests.Session.post()
        :return: dict with data
        """
        return super().post(url=f"{self.api_url}{endpoint}", data=data, json=json, **kwargs).json()

    def get_guild(self, guild_id) -> Guild:
        """
        Get Guild object from guild id
        :param guild_id: Discord guild id
        :return: discord_selfbot.Guild
        """
        return Guild(self.get(f"/guilds/{guild_id}"))

    def get_channel(self, channel_id) -> Channel:
        """
        Get Channel object from channel id
        :param channel_id: Discord channel id
        :return: discord_selfbot.Channel
        """
        return Channel(self.get(f"/channels/{channel_id}"))

    def get_me(self):
        return User(self.get("/users/@me"))

    def get_user(self, user_id):
        return User(self.get(f"/users/{user_id}"))
