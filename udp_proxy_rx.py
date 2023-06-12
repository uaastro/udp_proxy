#!/usr/bin/python3

import socket
import struct

UDP_MAX_PKT_SIZE=2048
UDP_IP_TX= "127.0.0.1"
UDP_PORT_TX = 5620
link_id = 1
pkt_num = 0

udp_streams = [
    {"ip": "127.0.0.1", "port": 5680},
    {"ip": "127.0.0.1", "port": 5681},
]

sock_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sockets = []
for stream in udp_streams:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(stream["ip"],' ',stream["port"])
    udp_socket.bind((stream["ip"], stream["port"]))
    udp_socket.setblocking(0)  # Установка неблокирующего режима
    sockets.append(udp_socket)

while True:
    for udp_socket in sockets:
        try:
            packet, addr = udp_socket.recvfrom(UDP_MAX_PKT_SIZE) 

            PACKET_SIZE = len(packet)
            link_id, packet_number, data= struct.unpack("!II"+str((PACKET_SIZE - 4 - 4))+"s", packet)
            #print (f"{link_id} {packet_number}")
            if packet_number > pkt_num:
                sock_tx.sendto(packet,(UDP_IP_TX, UDP_PORT_TX))
                #print (udp_socket.getsockname(),' pkt_num: ',pkt_num," packet_number: ",packet_number)
                pkt_num=packet_number
            else:
                #print ('--> ',udp_socket.getsockname(),' pkt_num: ',pkt_num," packet_number: ",packet_number)
        except socket.error:
            continue
