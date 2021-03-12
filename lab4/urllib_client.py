import socket
import configparser
import requests
import concurrent.futures
import urllib.request


class Client:
    __HOST: str = None
    __PORT: int = None
    cities = ["Moscow", "Minsk", "London", "Kiev"]

    def load_settings(self):
        configs = configparser.ConfigParser()
        configs.read("Configs/configs.ini")
        self.__HOST = configs["client"]["host"]
        self.__PORT = int(configs["client"]["port"])

    def integration_test(self):
        myurls = [f"http://{self.__HOST}:65432/temperature?city={city}" for city in self.cities]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(
                    lambda: urllib.request.urlopen(f"http://{self.__HOST}:65432/temperature?city={city}").read())
                for city in self.cities]

        results = [f.result() for f in futures]

        print("Results: %s" % results)
        # responses = []
        # data = []
        # for myurl in myurls:
        #     data.append(urllib.request.urlopen(myurl).read())
        #
        # # Output from the GET assuming response code was 200
        # # for response in responses:
        # #     data.append(response.read())
        #
        # for row in data:
        #     print(row)

    def __init__(self):
        self.load_settings()


if __name__ == "__main__":
    client = Client()
    client.integration_test()
