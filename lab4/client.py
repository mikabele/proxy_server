#!/usr/bin/env python3

import socket

HOST = 'localhost'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

city = input()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    query_str = city.encode("utf-8")
    #print(bytes(city))
    s.sendall(query_str)
    data = s.recv(1024)

    #print('Received', repr(data))
