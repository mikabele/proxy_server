import socket
import threading
import requests


class ProxyServer:
    __api_key = "7e47aaf7a09ef12d041a22ab370175d0"
    __cache_size = 3
    __cached_requests: list[tuple[str, int]] = list()
    __HOST = ''
    __PORT = 65432

    def get_query_result(self, city: str) -> int:
        """
        Возвращает температуру, полученую с сервера

        :param city: город, где измеряется температура
        :return: температура
        """
        params = dict(access_key=self.__api_key, query=city)
        req = requests.get("http://api.weatherstack.com/current", params=params)
        temperature = eval(req.text)["current"]["temperature"]
        self.cache_request(city, temperature)
        return temperature

    def process_client_query(self, client_socket: socket.socket, client_address: str) -> None:
        """
        Обрабатывает запрос клиента

        :param client_socket:
        :param client_address:
        :return:
        """
        with client_socket:
            print('Connected by', client_address)
            city = str(client_socket.recv(1024))[2:-1]
            temperature = self.get_cached_request(city)
            if not temperature:
                print("not from cached requests")
                temperature = self.get_query_result(city)
            else:
                temperature = temperature[1]
            client_socket.sendall(bytes(str(temperature), encoding="UTF-8"))

    def cache_request(self, requested_place: str, request_info: int) -> None:
        """Кэширует запрос.

        :param requested_place:     название города из зароса.
        :param request_info:        температура в запрашиваемом городе.
        :return:
        """
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
        """ Возвращает запрос из кэшированных запросов для соответствующего города.

        :param requested_place: Название города, по которому делается запрос
        :return: Если requested_place найдено возвращает последний запрос сделанный для данного города. Иначе - None.
        """
        for place, info in self.__cached_requests:
            if requested_place == place:
                return place, info
        return None

    def connect_to_server(self):
        """
        Подключает клиента к прокси-серверу

        :return:
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen(2)
            while True:
                client_socket, client_address = s.accept()
                client_thread = threading.Thread(name=client_address, target=self.process_client_query,
                                                 args=(client_socket, client_address))
                client_thread.setDaemon(True)
                client_thread.start()


if __name__ == "__main__":
    proxy = ProxyServer()
    proxy.connect_to_server()
