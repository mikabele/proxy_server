import socket
import threading
import requests


class ProxyServer:
    __api_key = "7e47aaf7a09ef12d041a22ab370175d0"
    __cache_size = 10
    __cached_requests = list()
    # Standard loopback interface address (localhost) If you pass an empty string,
    # the server will accept connections on all available IPv4 interfaces.
    __HOST = ''
    __PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    def create_get_query(self, city: str):
        params = dict(access_key=self.__api_key, query=city)
        req = requests.get("http://api.weatherstack.com/current", params=params)
        temperature = eval(req.text)["current"]["temperature"]
        self.cache_request(city, temperature)
        return temperature

    def process_client_query(self, client_socket, client_address):
        with client_socket:
            print('Connected by', client_address)
            city = str(client_socket.recv(1024))[2:-1]
            temperature = self.get_cached_request(city)[1]
            if not temperature:
                temperature = self.create_get_query(city)
            client_socket.sendall(bytes(str(temperature), encoding="UTF-8"))

    def cache_request(self, requested_place: str, request_info: int) -> None:
        """Кэширует запрос.

        :param requested_place:     название города из зароса.
        :param request_info:        температура в запрашиваемом городе.
        :return:
        """
        if len(self.__cached_requests) == self.__cache_size:
            contains_requested_pace = False
            for place, info in self.__cached_requests:
                if requested_place == place:
                    contains_requested_pace = True
                    self.__cached_requests.remove([place, info])
                    break
            if not contains_requested_pace:
                del self.__cached_requests[-1]
        self.__cached_requests.append(list(requested_place, request_info))

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
        print(socket.AF_INET, socket.SOCK_STREAM)
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
