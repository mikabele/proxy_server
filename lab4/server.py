# # #!/usr/bin/python
# #
# # # This is a simple port-forward / proxy, written using only the default python
# #
# # # library. If you want to make a suggestion or fix something you can contact-me
# #
# # # at voorloop_at_gmail.com
# #
# # # Distributed over IDC(I Don't Care) license
# #
# # import socket
# #
# # import select
# #
# # import time
# #
# # import sys
# #
# # # Changing the buffer_size and delay, you can improve the speed and bandwidth.
# #
# # # But when buffer get to high or delay go too down, you can broke things
# #
# # buffer_size = 4096
# #
# # delay = 0.0001
# #
# # forward_to = ('google.com', 25)
# #
# #
# # class Forward:
# #
# #     def __init__(self):
# #
# #         self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #
# #     def start(self, host, port):
# #
# #         try:
# #
# #             self.forward.connect((host, port))
# #
# #             return self.forward
# #
# #         except Exception as e:
# #
# #             print(e)
# #
# #             return False
# #
# #
# # class TheServer:
# #     input_list = []
# #
# #     channel = {}
# #
# #     def __init__(self, host, port):
# #
# #         self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #
# #         self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# #
# #         self.server.bind((host, port))
# #
# #         self.server.listen(200)
# #
# #     def main_loop(self):
# #
# #         self.input_list.append(self.server)
# #
# #         while 1:
# #
# #             time.sleep(delay)
# #
# #             ss = select.select
# #
# #             inputready, outputready, exceptready = ss(self.input_list, [], [])
# #
# #             for self.s in inputready:
# #
# #                 if self.s == self.server:
# #                     self.on_accept()
# #
# #                     break
# #
# #                 self.data = self.s.recv(buffer_size)
# #
# #                 if len(self.data) == 0:
# #
# #                     self.on_close()
# #
# #                     break
# #
# #                 else:
# #
# #                     self.on_recv()
# #
# #     def on_accept(self):
# #
# #         forward = Forward().start(forward_to[0], forward_to[1])
# #
# #         clientsock, clientaddr = self.server.accept()
# #
# #         if forward:
# #
# #             print(clientaddr, "has connected")
# #
# #             self.input_list.append(clientsock)
# #
# #             self.input_list.append(forward)
# #
# #             self.channel[clientsock] = forward
# #
# #             self.channel[forward] = clientsock
# #
# #         else:
# #
# #             print("Can't establish connection with remote server.")
# #
# #             print("Closing connection with client side", clientaddr)
# #
# #             clientsock.close()
# #
# #     def on_close(self):
# #
# #         print(self.s.getpeername(), "has disconnected")
# #
# #         # remove objects from input_list
# #
# #         self.input_list.remove(self.s)
# #
# #         self.input_list.remove(self.channel[self.s])
# #
# #         out = self.channel[self.s]
# #
# #         # close the connection with client
# #
# #         self.channel[out].close()  # equivalent to do self.s.close()
# #
# #         # close the connection with remote server
# #
# #         self.channel[self.s].close()
# #
# #         # delete both objects from channel dict
# #
# #         del self.channel[out]
# #
# #         del self.channel[self.s]
# #
# #     def on_recv(self):
# #
# #         data = self.data
# #
# #         # here we can parse and/or modify the data before send forward
# #
# #         print(data)
# #
# #         self.channel[self.s].send(data)
# #
# #
# # if __name__ == '__main__':
# #
# #     server = TheServer('0.0.0.0', 9090)
# #
# #     try:
# #
# #         server.main_loop()
# #
# #     except KeyboardInterrupt:
# #
# #         print("Ctrl C - Stopping server")
# #
# #         sys.exit(1)
#
# imporr
#
# def __init__(self, config):
#     # Shutdown on Ctrl+C
#     signal.signal(signal.SIGINT, self.shutdown)
#
#     # Create a TCP socket
#     self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#     # Re-use the socket
#     self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#
#     # bind the socket to a public host, and a port
#     self.serverSocket.bind((config['HOST_NAME'], config['BIND_PORT']))
#
#     self.serverSocket.listen(10) # become a server socket
#     self.__clients = {}
#
# while True:
#
#     # Establish the connection
#     (clientSocket, client_address) = self.serverSocket.accept()
#
#     d = threading.Thread(name=self._getClientName(client_address),
#     target = self.proxy_thread, args=(clientSocket, client_address))
#     d.setDaemon(True)
#     d.start()
#
# # get the request from browser
# request = conn.recv(config['MAX_REQUEST_LEN'])
#
# # parse the first line
# first_line = request.split('\n')[0]
#
# # get url
# url = first_line.split(' ')[1]
#
#
# http_pos = url.find("://") # find pos of ://
# if (http_pos==-1):
#     temp = url
# else:
#     temp = url[(http_pos+3):] # get the rest of url
#
# port_pos = temp.find(":") # find the port pos (if any)
#
# # find end of web server
# webserver_pos = temp.find("/")
# if webserver_pos == -1:
#     webserver_pos = len(temp)
#
# webserver = ""
# port = -1
# if (port_pos==-1 or webserver_pos < port_pos):
#
#     # default port
#     port = 80
#     webserver = temp[:webserver_pos]
#
# else: # specific port
#     port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
#     webserver = temp[:port_pos]
#
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.settimeout(config['CONNECTION_TIMEOUT'])
# s.connect((webserver, port))
# s.sendall(request)
#
# while 1:
#     # receive data from web server
#     data = s.recv(config['MAX_REQUEST_LEN'])
#
#     if (len(data) > 0):
#         conn.send(data) # send to browser/client
#     else:
#         break
import socket
import threading
import time
import requests

api_key = "7e47aaf7a09ef12d041a22ab370175d0"


def create_get_query(city: str):
    params = dict(key=api_key, query=city)
    print(params)
    req = requests.get("http://api.weatherstack.com/current", params=params)
    print(req.text)
    return req.text


def process_client_query(client_socket: socket.socket, client_address):
    with client_socket:
        # while True:
        print('Connected by', client_address)
        # time.sleep(5)
        city = ""
        i = 0
        while True:
            data = client_socket.recv(1024)
            print(data)
            if not data:
                break
            city += str(data)
            print(city)
            i += 1
            print(i)
        params = dict(key=api_key, query=city)
        print(params)
        req = requests.get("http://api.weatherstack.com/current", params=params)
        print(req.text)
        weather = req.text
        client_socket.sendall(bytes(weather))


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
        # client_thread = threading.Thread(name=addr, target=process_client_query, args=(conn, addr))
        # client_thread.setDaemon(True)
        # client_thread.start()
        with client_socket:
            # while True:
            print('Connected by', client_address)
            # time.sleep(5)
            city = ""
            i = 0
            while True:
                data = client_socket.recv(1024)
                print(data)
                if not data:
                    break
                city += str(data)
                print(city)
                i += 1
                print(i)
                client_socket.sendall(b"Minsk")
            params = dict(access_key=api_key, query=city[2:-1])
            print(params)
            req = requests.get("http://api.weatherstack.com/current", params=params)
            print(req.text)
            weather = req.text
            client_socket.sendall(bytes(weather,encoding="UTF-8"))
