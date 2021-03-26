import requests
import os
import dotenv
import grequests
from gevent import monkey as curious_george
import urllib3.util.ssl_
from requests import Session

from lab4.handlers.RequestHandler import RequestHandler
from lab4.RequestResult import RequestResult


class WeatherHandler(RequestHandler):
    __api_key: str = "7e47aaf7a09ef12d041a22ab370175d0"
    __classname__: str = "weather"

    def __load_settings(self):
        dotenv.load_dotenv(".env")
        #self.__api_key = os.environ.get("api_key")

    async def handle_request(self, func: str, args: dict[str, str]) -> RequestResult:
        if "city" not in args.keys():
            return None
        params = dict(access_key=self.__api_key, query=args["city"])
        # сделать асинхронным
        req = self.session.get(
            url=f"http://api.weatherstack.com/current?access_key={self.__api_key}&query={args['city']}")
        #print(req.url)
        print(eval(req.content))
        if func not in req.keys():
            return None
        return RequestResult(req[func])

    def __init__(self):
        self.__load_settings()
        curious_george.patch_all(thread=False, select=False)
        self.session = Session()

    def get_classname(self) -> str:
        return self.__classname__
