class WsMessage:
    def __init__(self, message_data: dict):
        self._message_data = message_data
        self.op = message_data["op"]
        self.title = message_data["t"]
        self.data = message_data["d"]


class MessageHandler:
    def __init__(self, callback, **kwargs):
        self.callback = callback
        self.kwargs = kwargs