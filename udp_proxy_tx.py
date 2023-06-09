#!/usr/bin/python3

import socket
import struct

UDP_MAX_PKT_SIZE=2048
UDP_IP_RX= "127.0.0.1"
UDP_PORT_RX = 5670
link_id = 1
pkt_num = 0

udp_streams = [
    {"ip": "127.0.0.1", "port": 5680},
    {"ip": "127.0.0.1", "port": 5681},
    # Добавьте остальные потоки в список udp_streams
]

#--init--


sock_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_rx.bind((UDP_IP_RX, UDP_PORT_RX))
#socket_rx.setblocking(0)  # Установка неблокирующего режима


while True:
    
    data, addr = sock_rx.recvfrom(UDP_MAX_PKT_SIZE)
    PACKET_SIZE = len(data)
    pkt_num += 1
    packet = struct.pack("!II"+str(PACKET_SIZE)+"s", link_id, pkt_num, data)
    
    for udp_stream in udp_streams:
        sock_tx.sendto(packet, (udp_stream["ip"], udp_stream["port"]))



