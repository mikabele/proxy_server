import asyncio
import configparser

from handlers import RequestHandler
from RequestResult import RequestResult
from collections import deque
from RequestParams import RequestParams

from handlers.WeatherHandler import WeatherHandler


class ProxyServer:

    def __load_settings(self):
        configs = configparser.ConfigParser()
        configs.read("Configs/configs.ini")
        self.__HOST = configs["server"]["host"]
        self.__PORT = int(configs["server"]["port"])
        self.__cache_size = int(configs["server"]["cache_size"])
        self.__threads_count = int(configs["server"]["threads_count"])

    def __get_request_params(self, request_str: str) -> RequestParams:
        main_info = request_str.split("\n")[0]
        params_str = main_info.split(" ")[1]
        handler, other_params = params_str[1:].split("/")
        func, args = other_params.split("?")
        args_dict = dict([pair.split("=") for pair in args.split("&")])
        return RequestParams(handler, func, args_dict)

    async def __handle_request(self, request: str) -> RequestResult:
        params = self.__get_request_params(request)
        handler = params.get_handler()
        func = params.get_func()
        args = params.get_args()
        requested_result = self.__get_cached_request(handler, func, args)
        if not requested_result:
            print("not from cached requests")
            result = await self.__request_handlers[handler].handle_request(func, args)
            if result is None:
                return "Error: invalid request"
            requested_result = result
            self.__cache_request(handler, func, args, requested_result)
        else:
            requested_result = requested_result
        return requested_result

    async def __process_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        request = await self.__read_request(reader)
        if request is None:
            print("Client unexpectedly disconnected")
        else:
            result = await self.__handle_request(request)
            await self.__write_result(writer, result)

    async def __write_result(self, writer: asyncio.StreamWriter, result: RequestResult) -> None:
        sending_str = self.get_sending_str(result)
        writer.write(bytearray(sending_str, encoding="UTF-8"))
        await writer.drain()
        writer.close()

    def get_sending_str(self, requested_result: RequestResult) -> str:
        return "HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body>" + str(
            requested_result) + "</body></html>\n"

    async def __read_request(self, reader: asyncio.StreamReader, delimiter=b'\r\n\r\n') -> str:
        request = bytearray()
        while True:
            chunk = await reader.read(4)
            if not chunk:
                # client disconnected prematurely
                break
            request += chunk
            if delimiter in request:
                return request.decode("UTF-8")

    def __cache_request(self, request: str, func: str, args: dict, request_info: RequestResult) -> None:
        func_and_args_str = func + str(args)
        if len(self.__cached_requests[request]) == self.__cache_size:
            contains_func_and_args_str = False
            for cached_func_and_args_str, cached_info in self.__cached_requests[request]:
                if func_and_args_str == cached_func_and_args_str:
                    contains_func_and_args_str = True
                    self.__cached_requests[request].remove((func_and_args_str, request_info))
                    break
            if not contains_func_and_args_str:
                del self.__cached_requests[request][0]
        self.__cached_requests[request].append((func_and_args_str, request_info))

    def __get_cached_request(self, request: str, func: str, args: dict) -> RequestResult:
        func_and_args_str = func + str(args)
        for cached_func_and_args_str, info in self.__cached_requests[request]:
            if cached_func_and_args_str == func_and_args_str:
                return info

    async def run_server(self):
        server = await asyncio.start_server(self.__process_client, self.__HOST, self.__PORT)
        await server.serve_forever()

    def __init__(self, handlers: list[RequestHandler]):
        self.__load_settings()
        self.__request_handlers = dict()
        self.__request_handlers = {handler().get_classname(): handler() for handler in handlers}
        self.__cached_requests = {x.get_classname(): deque() for x in self.__request_handlers.values()}


if __name__ == "__main__":
    proxy = ProxyServer([WeatherHandler])
    asyncio.run(proxy.run_server())
