import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

from .exceptions import WrongWebSocketMessage
from .service import market


class CryptoMarketConsumer(WebsocketConsumer):
    def connect(self) -> None:
        headers = self.scope["headers"]
        token_str = None
        user = AnonymousUser()
        for header in headers:
            if header[0] == b"cookie":
                if b'Authorization' in header[1]:
                    auth_name, token_str = header[1].decode().split("=")
                    break

        if token_str is not None and len(token_str) > 0:
            try:
                token_name, token_key = token_str.split()
                if token_name == "Token":
                    token = Token.objects.get(key=token_key)
                    user = token.user
            except Token.DoesNotExist:
                print("Cannot find token!")

        if user.is_authenticated:
            self.accept()

    def disconnect(self, code) -> None:
        print("Disconnected")

    def receive(self, text_data=None, bytes_data=None) -> None:
        if text_data == "get_exchange_rate":
            exchange_rate = market.get_exchange_rate()
            self.send(text_data=str(exchange_rate))
        else:
            self.send(text_data="wrong_msg")