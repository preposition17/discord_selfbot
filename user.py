class User:
    def __init__(self, user_data: dict):
        self._user_data = user_data

        self.id = self._user_data["id"]
        self.username = self._user_data["id"]
        self.discriminator = self._user_data["discriminator"]
        self.fullname = f"{self.username}@{self.discriminator}"