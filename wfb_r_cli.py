#!/usr/bin/python3

import re
import time
import socket

from rich.console import Console
from rich.theme import Theme
from rich.live import Live
from rich.table import Table
from rich import box

data = """
2435863 ANT 301 527:-4:15:16
2435863 ANT 201 527:16:16:16
2435863 ANT 200 527:16:16:16
2435863 ANT 101 702:-6:15:16
2435863 ANT 100 702:16:16:16
2435863 ANT 300 527:6:15:16
2435863 ANT 1 707:-22:-16:-12
2435863 ANT 0 707:-22:-16:-14
2435863 PKT 2467:0:2467:1:0:0
2436864 ANT 301 525:-6:15:16
2436864 ANT 201 525:4:15:16
2436864 ANT 200 525:16:16:16
2436864 ANT 101 715:-8:14:16
2436864 ANT 100 715:16:16:16
2436864 ANT 300 525:0:15:16
2436864 ANT 1 715:-22:-15:-8
2436864 ANT 0 715:-22:-16:-10
2436864 PKT 2484:0:2484:0:0:0
2437865 ANT 301 525:6:15:16
2437865 ANT 201 525:-2:15:16
2437865 ANT 200 525:4:15:16
2437865 ANT 101 708:-4:15:16
2437865 ANT 100 708:16:16:16
2437865 ANT 300 525:16:16:16
2437865 ANT 1 712:-20:-15:-10
2437865 ANT 0 712:-22:-15:-12
2437865 PKT 2474:0:2474:1:0:0
2438866 ANT 301 525:16:16:16
2438866 ANT 201 525:16:16:16
2438866 ANT 200 525:4:15:16
2438866 ANT 101 721:-6:15:16
2438866 ANT 100 721:16:16:16
2438866 ANT 300 525:16:16:16
2438866 ANT 1 721:-22:-15:-10
2438866 ANT 0 721:-18:-15:-12
2438866 PKT 2496:0:2496:0:0:0
2439867 ANT 301 524:-8:11:16
2439867 ANT 201 524:16:16:16
2439867 ANT 200 524:16:16:16
2439867 ANT 101 698:-10:11:16
2439867 ANT 100 698:-4:15:16
2439867 ANT 300 524:-4:14:16
2439867 ANT 1 706:-26:-17:-12
2439867 ANT 0 706:-24:-16:-14
2439867 PKT 2454:0:2454:2:0:0
2440868 ANT 101 683:-6:12:16
2440868 ANT 100 683:-6:14:16
2440868 ANT 0 684:-22:-17:-12
2440868 ANT 301 525:-12:-2:16
2440868 ANT 1 684:-28:-21:-16
2440868 ANT 300 525:-2:14:16
2440868 ANT 201 525:-10:11:16
2440868 ANT 200 525:-4:15:16
2440868 PKT 2420:0:2420:0:0:0
2441869 ANT 301 525:-12:-4:16
2441869 ANT 201 525:-6:12:16
2441869 ANT 200 525:-4:15:16
2441869 ANT 101 691:-6:14:16
2441869 ANT 100 691:-6:12:16
2441869 ANT 300 525:-2:14:16
2441869 ANT 1 691:-24:-18:-14
2441869 ANT 0 691:-26:-17:-14
2441869 PKT 2436:0:2436:0:0:0
2442869 ANT 101 715:-2:15:16
2442869 ANT 100 715:-6:11:16
2442869 ANT 0 720:-22:-18:-16
2442869 ANT 301 525:-8:-3:16
2442869 ANT 1 720:-24:-21:-16
2442869 ANT 300 525:-4:13:16
2442869 ANT 201 525:-8:4:16
2442869 ANT 200 525:-2:15:16
2442869 PKT 2489:0:2489:0:0:0
2443870 ANT 301 525:-8:1:16
2443870 ANT 201 525:-6:4:16
2443870 ANT 200 525:-8:14:16
2443870 ANT 101 710:-2:15:16
2443870 ANT 100 710:-6:15:16
2443870 ANT 300 525:-4:14:16
2443870 ANT 1 717:-24:-20:-16
2443870 ANT 0 717:-22:-18:-14
2443870 PKT 2481:0:2481:0:0:0
2444871 ANT 301 525:-8:4:16
2444871 ANT 201 525:-10:3:16
2444871 ANT 200 525:-6:14:16
2444871 ANT 101 712:-4:15:16
2444871 ANT 100 712:0:15:16
2444871 ANT 300 525:-2:15:16
2444871 ANT 1 716:-24:-20:-16
2444871 ANT 0 716:-20:-16:-14
2444871 PKT 2482:0:2482:0:0:0
2445875 ANT 301 526:-6:4:16
2445875 ANT 201 527:-6:8:16
2445875 ANT 200 527:2:15:16
2445875 ANT 101 725:0:15:16
2445875 ANT 100 725:4:15:16
2445875 ANT 300 526:2:15:16
2445875 ANT 1 727:-22:-20:-18
2445875 ANT 0 727:-18:-16:-14
2445875 PKT 2509:0:2509:1:0:0
2446875 ANT 201 524:-4:13:16
2446875 ANT 200 524:4:15:16
2446875 ANT 101 688:16:16:16
2446875 ANT 100 688:16:16:16
2446875 ANT 0 692:-18:-16:-14
2446875 ANT 301 525:-6:3:16
2446875 ANT 1 692:-24:-21:-18
2446875 ANT 300 525:4:15:16
2446875 PKT 2433:0:2433:2:0:0
2447875 ANT 101 685:4:15:16
2447875 ANT 100 685:8:15:16
2447875 ANT 0 689:-18:-16:-16
2447875 ANT 301 525:-6:3:14
2447875 ANT 1 689:-24:-21:-18
2447875 ANT 300 525:4:15:16
2447875 ANT 201 525:-2:14:16
2447875 ANT 200 525:16:16:16
2447875 PKT 2428:0:2428:0:0:0
2448877 ANT 301 528:-6:3:14
2448877 ANT 201 529:-4:13:16
2448877 ANT 200 529:6:15:16
2448877 ANT 101 708:2:15:16
2448877 ANT 100 708:16:16:16
2448877 ANT 300 528:4:15:16
2448877 ANT 1 715:-22:-20:-18
2448877 ANT 0 715:-18:-16:-16
2448877 PKT 2484:0:2484:0:0:0
2449878 ANT 201 522:-6:11:16
2449878 ANT 200 522:-2:15:16
2449878 ANT 101 694:16:16:16
2449878 ANT 100 694:4:15:16
2449878 ANT 0 720:-18:-16:-14
2449878 ANT 301 523:-8:0:16
2449878 ANT 1 720:-24:-21:-18
2449878 ANT 300 523:0:15:16
2449878 PKT 2462:0:2462:2:0:0
2450879 ANT 301 528:-10:-6:12
"""
def main ():
    
    
    def print_status(d_pkt, d_fec_r, d_pkts, d_pkt_lost, d_d_err, d_fec_r_s, d_pkt_lost_s, d_d_err_s, d_ant_data) -> Table:
        
        table_main = Table(expand=True,show_header=False,highlight=
                      True,box= None)
        table_main.add_column("PKT")
        table_main.add_column("RSSI")
        
        table_pkt = Table(show_header=True,highlight=
                      True,box=box.ROUNDED)
        
        table_pkt.add_column("[RX]")
        table_pkt.add_column("pkt/s")
        table_pkt.add_column("pkt")
        
        table_pkt.add_row("recv",f"{d_pkts}",f"{d_pkt}")
        table_pkt.add_row("fec_r",f"{d_fec_r_s}", f"{d_fec_r}")
        table_pkt.add_row("lost",f"{d_pkt_lost_s}",f"{d_pkt_lost}")
        table_pkt.add_row("d_err",f"{d_d_err_s}",f"{d_d_err}")
        
        table_rssi = Table(show_header=True,highlight=
                      True,box=box.ROUNDED) #box.ASCII2
        
        table_rssi.add_column("[ANT]")
        table_rssi.add_column("pkt/s",justify="right")
        table_rssi.add_column("RSSI",justify="center")
        
        for ant in ant_data:
            d_rssi_min = ant["rssi_min"]
            d_rssi_avg = ant["rssi_avg"]
            d_rssi_max = ant["rssi_max"]
            d_ant_num = ant["ant_num"]
            d_ant_pkts = ant["pkts"]
            
            table_rssi.add_row(f"[grey58]{d_ant_num}[/]",f"{d_ant_pkts}",f"{d_rssi_min:3} < {d_rssi_avg:3} < {d_rssi_max:3}")
        
        table_main.add_row(table_pkt,table_rssi)
        
        return table_main       
        
    #lines = data.strip().split("\n")
    
    UDP_IP = "127.0.0.1"
    UDP_PORT = 14550

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    
    ant_data = []
    pkt = 0
    fec_r = 0
    pkt_lost = 0
    d_err = 0
    wlan_number = 4
    pkts_1 = 0
    zero = 0
    pkts = 0
    fec_r_s = 0
    pkt_lost_s =0
    d_err_s = 0

    for i in range(wlan_number):
        ant_data.append({"ant_num": i*100,"pkts": 0, "rssi_min": 0, "rssi_avg": 0, "rssi_max": 0})
        ant_data.append({"ant_num": i*100+1,"pkts": 0, "rssi_min": 0, "rssi_avg": 0, "rssi_max": 0})
    
    console = Console()

    console.print("\n")
    console.rule("WFBR-CLI") 
    console.print("")
    #---------------------------------------------------------------------------------------------------
    
    with Live(print_status(0,0,0,0,0,0,0,0,ant_data), refresh_per_second=4) as live:
        
        while True:
            data, addr = sock.recvfrom(256)  # Получаем данные из UDP пакета
            line = data.decode("utf-8")
            live.console.print(line.split())
            parts = re.split(r"\s+", line)
            if parts[1] == "ANT":
                ant_num = int(parts[2])
                pkts, rssi_min, rssi_avg, rssi_max = map(int, parts[3].split(":"))
                for i in range(wlan_number*2):
                    if ant_num == ant_data[i]["ant_num"]: 
                      ant_data[i]["pkts"] = pkts
                      ant_data[i]["rssi_min"] = rssi_min
                      ant_data[i]["rssi_avg"] = rssi_avg
                      ant_data[i]["rssi_max"] = rssi_max
                live.update(print_status(pkt, fec_r, pkts, pkt_lost, d_err, fec_r_s, pkt_lost_s, d_err_s,ant_data))
            elif parts[1] == "PKT":
                pkts_1, zero, pkts, fec_r_s, pkt_lost_s, d_err_s = map(int, parts[2].split(":"))
                pkt+= pkts
                fec_r+= fec_r_s 
                pkt_lost+= pkt_lost_s
                d_err+= d_err_s
                live.update(print_status(pkt, fec_r, pkts, pkt_lost, d_err, fec_r_s, pkt_lost_s, d_err_s,ant_data))

if __name__ == '__main__':
    main()
