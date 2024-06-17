from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from requests import post

from .model import Model, Field
from .callback import Callback

if TYPE_CHECKING:
    from .component import Multiplayer


class Response(Model):
    status: str = Field()
    result: dict = Field()


class Api:
    token: Optional[str]
    username: Optional[str]
    component: Multiplayer

    def __init__(self, component: Multiplayer) -> None:        
        self.token = None
        self.username = None
        self.component = component

        for k in self.__class__.__dict__.keys():
            if k.startswith("api_"):
                setattr(self, k, getattr(self, k))

    def api_login(self, username: str, password: str) -> Callback:
        return self.request("login", {
            "username": username,
            "password": password
        })

    def api_register(self, username: str, password: str) -> Callback:
        return self.request("register", {
            "username": username,
            "password": password
        })

    def on(self, method: str, **data) -> None:
        f = getattr(self.component, "on_" + method, None)

        if f:
            f(**data)

    def error(self, method: str, status: str) -> None:
        f = getattr(self.component, "error_" + method, None)

        if f:
            f(status)

    def request(self, method: str, data: dict) -> Callback:
        return Callback(
            self.post_request, method, 
            {
                "data": data,
                "token": self.token
            }
        )

    def post_request(self, method: str, json: dict) -> None:
        response = Response(**post(f"http://localhost:8080/api/{method}", json=json).json())

        if response.status == "ok":
            self.on(method, **response.result)
        else:
            self.error(method, response.status)
