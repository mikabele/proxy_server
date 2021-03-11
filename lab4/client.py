import socket
import configparser


class Client:
    __HOST: str = None
    __PORT: int = None

    def load_settings(self):
        configs = configparser.ConfigParser()
        configs.read("Configs/configs.ini")
        self.__HOST = configs["client"]["host"]
        self.__PORT = int(configs["client"]["port"])

    def main(self):
        city = input()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.__HOST, self.__PORT))
            query_str = city.encode("utf-8")
            s.sendall(query_str)
            data = s.recv(1024)

            print('Received', repr(data))


if __name__ == "__main__":
    client = Client()
    client.main()
