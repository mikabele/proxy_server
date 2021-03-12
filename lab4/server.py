import socket
import requests
import os
import dotenv
import configparser
from concurrent.futures import ThreadPoolExecutor
import LockingList


class ProxyServer:
    __api_key: str = None
    __cache_size: int = None
    __cached_requests: LockingList.LockingList = None
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

    def get_requested_result_from_remote_server(self, city: str) -> dict[str, object]:
        params = dict(access_key=self.__api_key, query=city)
        req = requests.get(url="http://api.weatherstack.com/current", params=params)
        return req.json()["current"]

    @staticmethod
    def get_request_params(request_str: str) -> tuple[str, dict[str, str]]:
        get_request = request_str.split("\n")[0]
        params_str = get_request.split(" ")[1]
        func, args = params_str.split("?")
        func = func[1:]
        args_dict = dict([pair.split("=") for pair in args.split("&")])
        return func, args_dict

    def handle_request(self, request: str, args: dict[str, str]) -> object:
        requested_result = self.get_cached_request(request, args["city"])
        if not requested_result:
            print("not from cached requests")
            result_dict = self.get_requested_result_from_remote_server(args["city"])
            if request not in result_dict:
                return "Error: invalid request"
            requested_result = result_dict[request]
            self.cache_request(request, args["city"], requested_result)
        else:
            requested_result = requested_result
        return requested_result

    def process_client_query(self, client_socket: socket.socket, client_address: str) -> None:
        with client_socket:
            request, args = self.get_request_params(client_socket.recv(1024).decode("utf-8"))
            #time.sleep(5)
            requested_result = self.handle_request(request, args)
            client_socket.sendall(bytes(self.get_sending_str(requested_result), encoding="UTF-8"))

    @staticmethod
    def get_sending_str(requested_result: object) -> str:
        return "HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body>" + str(
            requested_result) + "</body></html>\n"

    def cache_request(self, request: str, requested_place: str, request_info: object) -> None:
        if len(self.__cached_requests) == self.__cache_size:
            contains_requested_place = False
            for cached_request, cached_place, info in self.__cached_requests:
                if cached_request == request and requested_place == cached_place:
                    contains_requested_place = True
                    self.__cached_requests.remove((request, cached_place, info))
                    break
            if not contains_requested_place:
                del self.__cached_requests[0]
        self.__cached_requests.append((request, requested_place, request_info))

    def get_cached_request(self, request: str, requested_place: str) -> object:
        for cached_request, place, info in self.__cached_requests:
            if requested_place == place and cached_request == request:
                return info

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen(2)
            with self.__threads_pool as executor:
                while True:
                    client_socket, client_address = s.accept()
                    executor.submit(self.process_client_query, client_socket=client_socket,
                                    client_address=client_address)

    def __init__(self):
        self.load_settings()
        self.__threads_pool = ThreadPoolExecutor(self.__threads_count)
        self.__cached_requests = LockingList.LockingList()


if __name__ == "__main__":
    proxy = ProxyServer()
    proxy.start_server()
