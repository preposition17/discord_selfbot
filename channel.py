class Channel:
    def __init__(self, channel_data: dict):
        """
        Discord channel object
        :param channel_data: channel data from Discord api
        """
        self.json = channel_data

        self.id = self.json["id"]
        self.name = self.json["name"]
        self.guild_id = self.json["guild_id"]