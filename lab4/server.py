import socket
import threading
import requests
import os
import dotenv
import configparser
from concurrent.futures import ThreadPoolExecutor
import re
import time


class ProxyServer:
    __api_key: str = None
    __cache_size: int = None
    __cached_requests: list[tuple[str, int]] = list()
    __threads_pool: ThreadPoolExecutor = None
    __threads_count: int = None
    __HOST: str = None
    __PORT: int = None

    def load_settings(self):
        configs = configparser.ConfigParser()
        configs.read("Configs/configs.ini")
        self.__HOST = configs["server"]["host"]
        self.__PORT = int(configs["server"]["port"])
        self.__cache_size = int(configs["server"]["cache_size"])
        self.__threads_count = int(configs["server"]["threads_count"])
        dotenv.load_dotenv(".env")
        self.__api_key = os.environ.get("api_key")

    def get_query_result(self, city: str) -> int:
        params = dict(access_key=self.__api_key, query=city)
        req = requests.get(url="http://api.weatherstack.com/current", params=params)
        temperature = req.json()["current"]["temperature"]
        self.cache_request(city, temperature)
        return temperature

    def process_client_query(self, client_socket: socket.socket, client_address: str) -> None:
        with client_socket:
            get_request = client_socket.recv(1024).decode("utf-8").split("\n")[0]
            params_str = get_request.split(" ")[1]
            func, args = params_str.split("?")
            func = func[1:]
            args_dict = dict([pair.split("=") for pair in args.split("&")])
            time.sleep(5)
            temperature = self.get_cached_request(args_dict["city"])
            if not temperature:
                print("not from cached requests")
                temperature = self.get_query_result(args_dict["city"])
            else:
                temperature = temperature[1]
            sending_str = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body>" + str(
                temperature) + "</body></html>\n"
            client_socket.sendall(bytes(sending_str, encoding="UTF-8"))

    def cache_request(self, requested_place: str, request_info: int) -> None:
        if len(self.__cached_requests) == self.__cache_size:
            contains_requested_place = False
            for place, info in self.__cached_requests:
                if requested_place == place:
                    contains_requested_place = True
                    self.__cached_requests.remove((place, info))
                    break
            if not contains_requested_place:
                del self.__cached_requests[0]
        self.__cached_requests.append((requested_place, request_info))

    def get_cached_request(self, requested_place: str):
        for place, info in self.__cached_requests:
            if requested_place == place:
                return place, info
        return None

    def connect_to_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen(2)
            with self.__threads_pool as executor:
                while True:
                    client_socket, client_address = s.accept()
                    # client_thread = threading.Thread(name=client_address, target=self.process_client_query,
                    #                                  args=(client_socket, client_address))
                    # client_thread.setDaemon(True)
                    # client_thread.start()
                    executor.submit(self.process_client_query, client_socket=client_socket,
                                    client_address=client_address)

    def __init__(self):
        self.load_settings()
        self.__threads_pool = ThreadPoolExecutor(self.__threads_count)


if __name__ == "__main__":
    proxy = ProxyServer()
    proxy.connect_to_server()
