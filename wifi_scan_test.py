#!/usr/bin/python3

from scapy.all import *

wlan ='wlx00c0cab1b0be'
channels =['36','40','44','48','52','56','60','64','100','104','108','112','116','120','124','128','132','136','140','144','149','153','157','161','165','169','173','177']

def packet_handler(packet):
    if packet.haslayer(Dot11):
        if packet.haslayer(RadioTap):
            radiotap = packet.getlayer(RadioTap)
            signal_strength = radiotap.dBm_AntSignal
            antenna = radiotap.antenna
            sender = packet.addr2
            print(f"Antenna: {antenna}, Signal Strength: {signal_strength}, Sender: {sender}")

# Запуск снифера

subprocess.run(f"ifconfig {wlan} down",shell=True, check=True)

subprocess.run(f"iw dev {wlan} set monitor otherbss",shell=True, check=True)

subprocess.run(f"iw reg set US",shell=True, check=True)

subprocess.run(f"ifconfig {wlan} up",shell=True, check=True)
# Установка канала

for channel in channels:
    
    subprocess.run(f"iw dev {wlan} set channel {channel} HT20",shell=True, check=True)
        
    packets = sniff(iface=wlan, timeout=0.1)
         # Анализируем принятые пакеты
    for packet in packets:
        # Проверяем, является ли пакет пакетом Wi-Fi
        if packet.haslayer(Dot11):
            mac_address = packet.addr2
            signal_strength = packet.dBm_AntSignal
                
            # Делайте собственную логику обработки пакетов
            #print(ls(packet))
            print(f"{mac_address} ATN: {signal_strength} dBm channel: {channel}")
            