#!/usr/bin/python3

import subprocess
import select
import time

from scapy.all import *


def scan_channels(interface):
    iface = interface
    wlan = iface
    
    subprocess.run(f"ifconfig {wlan} down",shell=True, check=True)

    subprocess.run(f"iw dev {wlan} set monitor otherbss",shell=True, check=True)

    subprocess.run(f"iw reg set US",shell=True, check=True)

    subprocess.run(f"ifconfig {wlan} up",shell=True, check=True)
    i = 0
    while True:
        # Установка канала
        channel=161
        subprocess.run(f"iw dev {wlan} set channel {channel} HT20",shell=True, check=True)
        
        # Принимаем пакеты в течение некоторого времени
        packets = sniff(iface=iface, timeout=1)
        
        # Анализируем принятые пакеты
        for packet in packets:
            # Проверяем, является ли пакет пакетом Wi-Fi
            if packet.haslayer(Dot11):
                mac_address = packet.addr3
                signal_strength = packet.dBm_AntSignal
                
                # Делайте собственную логику обработки пакетов
                #print(ls(packet))
                print(f"{i}: {mac_address} ATN: {signal_strength} dBm channel: {channel}")
        i+=1
scan_channels("wlx00c0cab1b0be")
