class Config:
    def __init__(
            self,
            token,
            capabilities=253,
            os="Windows",
            os_version: str = "10",
            browser="Chrome",
            browser_version="99.0.4844.82",
            device="",
            locale="ru-RU",
            useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
            status="online",
            afk=False,
            api_version=9,
    ):
        """
        Config object for discord_selfbot.SelfBot and discord_selfbot.Api
        :param token: your discord user token
        :param capabilities: discord capabilities
        :param os: os, etc. "Windows"
        :param os_version: etc. "10"
        :param browser: etc. "Chrome"
        :param browser_version: browser version
        :param device:
        :param locale: etc. "en-En"
        :param useragent: browser useragent
        :param status: etc. "online"
        :param afk:
        :param api_version: etc. "9"
        """
        self.token = token
        self.capabilities = capabilities
        self.os = os
        self.os_version = os_version
        self.browser = browser
        self.browser_version = browser_version
        self.device = device
        self.locale = locale
        self.useragent = useragent
        self.status = status
        self.afk = afk

        self.api_version = api_version
        self.api_url = f"https://discord.com/api/v{self.api_version}"

    @property
    def json(self) -> dict:
        """
        Get config as json object
        :return: config as json object
        """
        return {
            "op": 2,
            "d": {
                "token": self.token,
                "capabilities": self.capabilities,
                "properties": {
                    "os": self.os,
                    "browser": self.browser,
                    "device": self.device,
                    "system_locale": self.locale,
                    "browser_user_agent": self.useragent,
                    "browser_version": self.browser_version,
                    "os_version": self.os_version,
                    "release_channel": "stable",
                    "client_build_number": 120390,
                    "client_event_source": False
                },
                "presence": {
                    "status": self.status,
                    "since": 0,
                    "activities": [],
                    "afk": self.afk
                },
                "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1
                }
            }
        }
