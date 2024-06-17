from typing import Callable
from functools import wraps
from flask import Flask, Response as FResponse, request, jsonify
from model import Field, Model


class Response(Model):
    status: str = Field()
    result: dict = Field()


class BaseApi:
    def __init__(self, app: Flask) -> None:
        self.tokens = {}

        for k in self.__class__.__dict__.keys():
            if k.startswith("api_") or k.startswith("apis_"):
                method = k[4:] if k.startswith('api_') else k[5:]
                router_method = f"/api/{method}"
            
                app.route(router_method, methods=["POST"])(self.handler(k, getattr(self, k)))

    def handler(self, method: str, function: Callable) -> Callable:
        @wraps(function)
        def f() -> FResponse:
            status = "ok"
            result = {}
            
            try:
                print(method, request.json)

                if method.startswith("apis_"):
                    result = function(**request.json["data"]) or {}
                else:
                    token = request.json.get("token")

                    if token is None:
                        raise ValueError("Не авторизирован")
                    
                    username = self.tokens.get(token)

                    if username is None:
                        raise ValueError("Токен недействителен")

                    result = function(**(request.json["data"] | { "username": username })) or {}
            except Exception as e:
                status = e.args[0]

            response = Response(status=status, result=result)

            return jsonify(response.to_json())
        
        return f
