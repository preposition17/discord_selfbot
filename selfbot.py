import traceback
from typing import Union
import zlib
import json
import random
import time
import threading

import rel
from websocket import WebSocketApp

from .config import Config
from .api import Api

from .utils import WsMessage
from .utils import MessageHandler

from .message import Message


class SelfBot:
    def __init__(self, token, config: Config = None):
        """
        Main SelfBot object based on websocket client
        :param token: your Discord user token
        :param config: discord_selfbot.Config instance
        """
        rel.safe_read()

        if config:
            self.config = config
        else:
            self.config = Config(token)

        self.api = Api.init(token, self.config)

        self.ZLIB_SUFFIX = b'\x00\x00\xff\xff'
        self.buffer = bytearray()
        self.inflator = zlib.decompressobj()

        self.ws = WebSocketApp("wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream",
                               on_open=self._on_ws_open,
                               on_message=self._on_ws_message,
                               on_error=self._on_ws_error,
                               on_close=self._on_ws_close)

        self.ping_loop_active = False
        self.identified = False

        self.token = token
        self.heartbeat_interval = None
        self.jitter = random.uniform(0, 1)
        self.ping_data = random.randint(17, 23)

        self.message_handlers = list()

    def _on_ws_message(self, ws, ws_message):
        self.buffer.extend(ws_message)

        if len(ws_message) < 4 or ws_message[-4:] != self.ZLIB_SUFFIX:
            return

        ws_message = self.inflator.decompress(self.buffer)
        ws_message = WsMessage(self._to_json(ws_message))
        self.buffer = bytearray()

        if ws_message.op == 10:
            if not self.identified:
                self._identify()
                self.identified = True
            if not self.ping_loop_active:
                self.heartbeat_interval = ws_message.data["heartbeat_interval"]
                self._start_ping()
                self.identified = True
            if self.identified and self.ping_loop_active:
                print("Ping!")
                self._send_message({
                "op": 1,
                "d": self.ping_data + random.randint(5, 10)
            })

        if ws_message.op == 0:
            if ws_message.title == "MESSAGE_CREATE":
                # print(ws_message.data)
                self._iter_message_handlers(Message(ws_message.data, self.api))

        self.on_ws_message(ws_message)

    def _on_ws_error(self, ws, error):
        print(traceback.format_exc())
        print("Error! ", error)

    def _on_ws_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def _on_ws_open(self, ws):
        print("Opened connection with Discord Gateway")

    def _to_json(self, data: Union[bytes, bytearray]):
        return json.loads(data.decode("utf-8"))

    def _ping_loop(self):
        time.sleep(5)
        while True:
            self._send_message({
                "op": 1,
                "d": self.ping_data
            })
            self.ping_data += random.randint(17, 23)
            time.sleep(self.heartbeat_interval * random.uniform(0, 1) / 1000)

    def _start_ping(self):
        ping_thread = threading.Thread(target=self._ping_loop)
        ping_thread.start()

    def _identify(self):
        self._send_message(self.config.json)
        print("Identified")

    def _send_message(self, data: dict):
        self.ws.send(json.dumps(data))

    def on_ws_message(self, message):
        """
        Called when receiving message from Discord websocket
        :param message: Discord websocket message
        """
        # print(message._message_data)
        pass

    def add_message_handler(self, callback, **kwargs):
        """
        Use callback functions for messages
        :param callback: your callback function
        :param kwargs: kwargs for callback
        """
        self.message_handlers.append(MessageHandler(callback, **kwargs))

    def _iter_message_handlers(self, message):
        for handler in self.message_handlers:
            handler.callback(message, **handler.kwargs)

    def run(self):
        """
        Run the Discord websocket client
        """
        self.ws.run_forever(dispatcher=rel)
        rel.signal(2, rel.abort)
        rel.dispatch()
