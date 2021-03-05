import socket
import threading
import requests

api_key = "7e47aaf7a09ef12d041a22ab370175d0"


def create_get_query(city: str):
    params = dict(access_key=api_key, query=city)
    req = requests.get("http://api.weatherstack.com/current", params=params)
    return req.text


cache_size = 10


def process_client_query(client_socket, client_address):
    with client_socket:
        # while True:
        print('Connected by', client_address)
        city = str(client_socket.recv(1024))[2:-1]
        weather = create_get_query(city)
        dictionary = eval(weather)
        temperature = dictionary['current']['temperature']
        client_socket.sendall(bytes(temperature, encoding="UTF-8"))


def cache_request(requested_place: str, request_info: int) -> None:
    """Кэширует запрос.

    :param requested_place:     название города из зароса.
    :param request_info:        температура в запрашиваемом городе.
    :return:
    """
    if len(cached_requests) == cache_size:
        contains_requested_pace = False
        for place, info in cached_requests:
            if requested_place == place:
                contains_requested_pace = True
                cached_requests.remove([place, info])
                break
        if not contains_requested_pace:
            del cached_requests[-1]
    cached_requests.append(list(requested_place, request_info))


def get_cached_request(requested_place: str):
    """ Возвращает запрос из кэшированных запросов для соответствующего города.

    :param requested_place: Название города, по которому делается запрос
    :return: Если requested_place найдено возвращает последний запрос сделанный для данного города. Иначе - None.
    """
    for place, info in cached_requests:
        if requested_place == place:
            return place, info
    return None


cached_requests = list()
# Standard loopback interface address (localhost) If you pass an empty string,
# the server will accept connections on all available IPv4 interfaces.
HOST = ''
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
print(socket.AF_INET, socket.SOCK_STREAM)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(2)
    while True:
        client_socket, client_address = s.accept()
        client_thread = threading.Thread(name=client_address, target=process_client_query,
                                         args=(client_socket, client_address))
        client_thread.setDaemon(True)
        client_thread.start()
