import socket
import requests
import os
import dotenv
import configparser
from concurrent.futures import ThreadPoolExecutor
import LockingList
import time
import asyncio
import sys
from RequestHandler import RequestHandler


class ProxyServer:
    __api_key: str = None
    __cache_size: int = None
    __cached_requests: dict[str, LockingList.LockingList] = None
    __threads_pool: ThreadPoolExecutor = None
    __threads_count: int = None
    __HOST: str = None
    __PORT: int = None
    __request_handlers: dict[str, RequestHandler] = None

    def load_settings(self):
        configs = configparser.ConfigParser()
        configs.read("Configs/configs.ini")
        self.__HOST = configs["server"]["host"]
        self.__PORT = int(configs["server"]["port"])
        self.__cache_size = int(configs["server"]["cache_size"])
        self.__threads_count = int(configs["server"]["threads_count"])
        dotenv.load_dotenv(".env")
        self.__api_key = os.environ.get("api_key")

    async def get_request_params(self, request_str: str) -> tuple[str, str, dict[str, str]]:
        main_info = request_str.split("\n")[0]
        params_str = main_info.split(" ")[1]
        handler, other_params = params_str.split("/")
        func, args = other_params.split("?")
        func = func[1:]
        args_dict = dict([pair.split("=") for pair in args.split("&")])
        return handler, func, args_dict

    async def handle_request(self, request: str) -> object:
        handler, func, args = await self.get_request_params(request)
        requested_result = await self.get_cached_request(handler, func, args)
        if not requested_result:
            print("not from cached requests")
            result = self.__request_handlers[handler].handle_request(func, args)
            if not result:
                return "Error: invalid request"
            requested_result = result
            await self.cache_request(handler, requested_result, args)
        else:
            requested_result = requested_result
        return requested_result

    async def process_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        request = await self.read_request(reader)
        if request is None:
            print("Client unexpectedly disconnected")
        else:
            result = await self.handle_request(request)
            await self.write_result(writer, result)

    async def write_result(self, writer: asyncio.StreamWriter, result: object) -> None:
        sending_str = await self.get_sending_str(result)
        writer.write(sending_str)
        await writer.drain()
        writer.close()

    async def get_sending_str(self, requested_result: object) -> bytearray:
        return bytearray("HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body>" + str(
            requested_result) + "</body></html>\n")

    async def read_request(self, reader: asyncio.StreamReader) -> str:
        request = bytearray()
        while True:
            chunk = await reader.read(4)
            if not chunk:
                # client disconnected prematurely
                break
            request += chunk
        return request.decode("UTF-8")

    async def cache_request(self, request: str, func: str, args: dict(), request_info: object) -> None:
        func_and_args_str = func + str(args)
        if request in self.__cached_requests:
            if len(self.__cached_requests) == self.__cache_size:
                contains_func_and_args_str = False
                for cached_func_and_args_str, cached_info in self.__cached_requests[request]:
                    if func_and_args_str == cached_func_and_args_str:
                        contains_func_and_args_str = True
                        self.__cached_requests[request].remove((func_and_args_str, request_info))
                        break
                if not contains_func_and_args_str:
                    del self.__cached_requests[request][0]
            self.__cached_requests.append((request, func_and_args_str, request_info))
        else:
            self.__cached_requests[request] = (func_and_args_str, request_info)

    async def get_cached_request(self, request: str, func: str, args: str) -> object:
        func_and_args_str = func + str(args)
        if request in self.__cached_requests:
            for cached_func_and_args_str, info in self.__cached_requests[request]:
                if cached_func_and_args_str == func_and_args_str:
                    return info

    async def run_server(self):
        server = await asyncio.start_server(self.proccess_client, self.__HOST, self.__PORT)
        await server.serve_forever()

    def __init__(self):
        self.load_settings()
        self.__threads_pool = ThreadPoolExecutor(self.__threads_count)
        self.__cached_requests = LockingList.LockingList()


if __name__ == "__main__":
    proxy = ProxyServer()
    asyncio.run(proxy.run_server())
