class Guild:
    def __init__(self, guild_data: dict):
        """
        Discord Guild object
        :param guild_data: guild data from Discord api
        """
        self.json = guild_data

        self.id = self.json["id"]
        self.name = self.json["name"]