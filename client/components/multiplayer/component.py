from utils import Component

from .api import Api
from .callback import Callback, current_callback


class Multiplayer(Component):
    api: Api
    
    def __init__(self, username: str, password: str) -> None:
        super().__init__()

        self.api = Api(self)

        self.register(username, password)
        
    def register(self, username: str, password: str) -> Callback:
        return self.api.api_register(username, password)

    def on_register(self) -> None:
        self.login(*current_callback().data.values())

    def error_register(self, status: str) -> None:
        self.login(*current_callback().data.values())

    def login(self, username: str, password: str) -> Callback:
        return self.api.api_login(username, password)

    def on_login(self, token: str) -> None:
        print(token)

    def error_login(self, status: str) -> None:
        print(status)
