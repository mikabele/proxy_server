import socket
import configparser
import requests
import concurrent.futures
import urllib.request


class Client:
    __HOST: str = None
    __PORT: int = None
    cities = ["Moscow", "Minsk", "London","Kiev","Hello"]

    def load_settings(self):
        configs = configparser.ConfigParser()
        configs.read("../Configs/configs.ini")
        self.__HOST = configs["client"]["host"]
        self.__PORT = int(configs["client"]["port"])

    def integration_test(self):
        myurls = [f"http://{self.__HOST}:65432/weather/temperature?city={city}" for city in self.cities]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(
                    lambda: requests.get(myurl))
                for myurl in myurls]

        results = [f.result().status_code for f in futures]
        print("Results: %s" % results)

    def __init__(self):
        self.load_settings()


if __name__ == "__main__":
    client = Client()
    client.integration_test()
