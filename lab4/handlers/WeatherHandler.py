import requests
import os
import dotenv

from lab4.handlers.RequestHandler import RequestHandler


class WeatherHandler(RequestHandler):
    __api_key: str = None
    __classname__: str = "weather"

    def load_settings(self):
        dotenv.load_dotenv(".env")
        self.__api_key = os.environ.get("api_key")

    async def handle_request(self, func: str, args: dict[str, str]) -> object:
        if "city" not in args.keys():
            return None
        params = dict(access_key=self.__api_key, query=args["city"])
        req = requests.get(url="http://api.weatherstack.com/current", params=params).json()["current"]
        #print(req)
        if func not in req.keys():
            return None
        return req[func]

    def __init__(self):
        self.load_settings()
