import requests
import os
import dotenv

import httpx
from lab4.handlers.RequestHandler import RequestHandler
from lab4.RequestResult import RequestResult


class WeatherHandler(RequestHandler):
    __api_key: str = None
    __classname__: str = "weather"

    def __load_settings(self):
        dotenv.load_dotenv(".env")
        self.__api_key = os.environ.get("api_key")

    async def handle_request(self, func: str, args: dict[str, str]) -> RequestResult:
        if "city" not in args.keys():
            return None
        params = dict(access_key=self.__api_key, query=args["city"])
        req = await self.__client.get(url="http://api.weatherstack.com/current", params=params)
        req = eval(req.content)['current']
        if func not in req.keys():
            return None
        return RequestResult(req[func])

    def __init__(self):
        self.__load_settings()
        self.__client = httpx.AsyncClient()

    def get_classname(self) -> str:
        return self.__classname__
