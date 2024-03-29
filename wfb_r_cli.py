#!/usr/bin/python3

import re
import time
import socket

from rich.console import Console
from rich.theme import Theme
from rich.live import Live
from rich.table import Table
from rich import box
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.rule import Rule
import click

@click.command()
@click.option('--ip', default="127.0.0.1", help='address of wfb server/default 127.0.0.1')
@click.option('--port', default=14550, help='port of wfb server/default 14550')
@click.option('--chname', default="rx_video", help='stat channel name/default rx_video')
@click.option('--shpkt', default="true", help='show pkt stat/default true')
@click.option('--shrssi', default="true", help='show rssi stat/default true')


def main (ip,port,chname,shpkt,shrssi):
    
    
    def print_status(d_pkt, d_fec_r, d_pkts, d_pkt_lost, d_d_err, d_fec_r_s, d_pkt_lost_s, d_d_err_s, d_ant_data) -> Table:
        
        table_main = Table(expand=True,show_header=False,highlight=
                      True,box= None, title="", title_style="white",title_justify="center")
        table_main.add_column(chname)
        #table_main.add_column("RSSI")
        table_main.add_row(Rule(title=chname))
        
        table_pkt = Table(show_header=True,highlight=
                      True,box=box.ROUNDED,style="blue")
        
        table_pkt.add_column("[RX]")
        table_pkt.add_column("pkt/s",justify="right")
        table_pkt.add_column("pkt",justify="right")
        
        table_pkt.add_row("recv",f"{d_pkts}",f"{d_pkt}")
        table_pkt.add_row("fec_r",f"{d_fec_r_s}", f"{d_fec_r}")
        table_pkt.add_row("lost",f"{d_pkt_lost_s}",f"{d_pkt_lost}")
        table_pkt.add_row("d_err",f"{d_d_err_s}",f"{d_d_err}")
        
        table_rssi = Table(show_header=True,highlight=
                      True,box=box.ROUNDED) #box.ASCII2
        
        table_rssi.add_column("[ANT]")
        table_rssi.add_column("pkt/s",justify="right")
        table_rssi.add_column("RSSI",justify="center")
        table_rssi.add_column("RSSI",justify="center")
        
        for ant in ant_data:
            d_rssi_min = ant["rssi_min"]
            d_rssi_avg = ant["rssi_avg"]
            d_rssi_max = ant["rssi_max"]
            d_ant_num = ant["ant_num"]
            d_ant_pkts = ant["pkts"]
            rssi_mlvl = 106 - abs(d_rssi_avg-16)
            d_total = 106
            if d_rssi_avg > -50:
                prgs_color='green'
            elif d_rssi_avg > -70:
                prgs_color='yellow'
            else:
                prgs_color='red'
            if d_ant_pkts == 0:
                prgs_color="grey58"
                #d_total = None
                rssi_mlvl =0
            progress = Progress(TextColumn("[progress.description]{task.description}"), BarColumn(complete_style=prgs_color,pulse_style="grey58"), TaskProgressColumn(text_format='[progress.percentage]{task.percentage:>3.0f}%',style='green'))
            task = progress.add_task(f"[grey58]{d_ant_num:3}", total=d_total)
            progress.update(task, completed=rssi_mlvl)
            table_rssi.add_row(f"[grey58]{d_ant_num}[/]",f"{d_ant_pkts}",f"{d_rssi_min:3} < {d_rssi_avg:3} < {d_rssi_max:3}",progress)
        
        if shpkt == "true":
            table_main.add_row(table_pkt)
        if shrssi == "true":
            table_main.add_row(table_rssi)
        
        return table_main       
        

    
    UDP_IP = ip
    UDP_PORT = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    #sock.setblocking(0) 
    
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
            #live.console.print(line.split())
            parts = re.split(r"\s+", line)
            if parts[0] == chname:
                live.console.print(line.split())
                if parts[2] == "ANT":
                    ant_num = int(parts[3])
                    pkts, rssi_min, rssi_avg, rssi_max = map(int, parts[4].split(":"))
                    for i in range(wlan_number*2):
                        if ant_num == ant_data[i]["ant_num"]: 
                            ant_data[i]["pkts"] = pkts
                            ant_data[i]["rssi_min"] = rssi_min
                            ant_data[i]["rssi_avg"] = rssi_avg
                            ant_data[i]["rssi_max"] = rssi_max
                    #live.update(print_status(pkt, fec_r, pkts, pkt_lost, d_err, fec_r_s, pkt_lost_s, d_err_s,ant_data))
                elif parts[2] == "PKT":
                    pkts_1, zero, pkts, fec_r_s, pkt_lost_s, d_err_s = map(int, parts[3].split(":"))
                    pkt+= pkts
                    fec_r+= fec_r_s 
                    pkt_lost+= pkt_lost_s
                    d_err+= d_err_s
                    live.update(print_status(pkt, fec_r, pkts, pkt_lost, d_err, fec_r_s, pkt_lost_s, d_err_s,ant_data))
                    ant_data = []
                    for i in range(wlan_number):
                        ant_data.append({"ant_num": i*100,"pkts": 0, "rssi_min": 0, "rssi_avg": 0, "rssi_max": 0})
                        ant_data.append({"ant_num": i*100+1,"pkts": 0, "rssi_min": 0, "rssi_avg": 0, "rssi_max": 0})
            
if __name__ == '__main__':
    main()
