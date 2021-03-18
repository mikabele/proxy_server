from RequestHandler import RequestHandler
import requests


class WeatherHandler(RequestHandler):
    __api_key: str = None

    def handle_request(self, func: str, args: dict[str, object]) -> str:
        params = dict(access_key=self.__api_key, query=city)
        req = requests.get(url="http://api.weatherstack.com/current", params=params)
        return req.json()["current"]
