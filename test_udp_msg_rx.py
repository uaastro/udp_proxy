#!/usr/bin/python3

import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 14550

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(256)  # Получаем данные из UDP пакета
    message = data.decode("utf-8")  # Раскодируем данные в строку
    print(message)
