import requests
import os
import dotenv

from lab4.handlers.RequestHandler import RequestHandler


class WeatherHandler(RequestHandler):
    __api_key: str = None
    __classname__: str = "weather"

    def load_settings(self):
        dotenv.load_dotenv("../.env")
        self.__api_key = os.environ.get("api_key")

    async def handle_request(self, func: str, args: dict[str, object]) -> object:
        if "city" not in args.keys():
            return "Error: args must have key 'city'"
        params = dict(access_key=self.__api_key, query=args["city"])
        req = requests.get(url="http://api.weatherstack.com/current", params=params).json()["current"]
        if func not in req.keys():
            return f"Error: request doesn't have info about '{func}'"
        return req[func]

    def __init__(self):
        self.load_settings()
