class WsMessage:
    def __init__(self):
        self._message_data = None
        self.op = None
        self.title = None
        self.data = None

    @classmethod
    def from_json(cls, message_data: dict):
        ws_message = cls()
        ws_message._message_data = message_data
        ws_message.op = message_data["op"]
        ws_message.title = message_data["t"] if "t" in message_data.keys() else None
        ws_message.data = message_data["d"]
        return ws_message

    @property
    def json(self):
        ws_message_json = {
            "op": self.op,
            "d": self.data
        }
        if self.title:
            ws_message_json["t"] = self.title
        return ws_message_json


class MessageHandler:
    def __init__(self, callback, **kwargs):
        self.callback = callback
        self.kwargs = kwargs

    def execute(self, message):
        self.callback(message, **self.kwargs)
