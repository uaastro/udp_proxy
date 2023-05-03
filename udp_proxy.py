import socket
import time
import struct

from rich.console import Console
from rich.theme import Theme
from rich.live import Live
from rich.table import Table
from rich import box

import sys
import select
import tty
import termios

import click

@click.command()
@click.option('--iprx', default="127.0.0.1", help='source ip address of udp server/default 127.0.0.1')
@click.option('--iptx', default="127.0.0.1", help='destination ip address of udp server/default 127.0.0.1')
@click.option('--portrx', default=5600, help='port of udp server/default 5600')
@click.option('--porttx', default=5602, help='port of udp server/default 5602')
@click.option('--mpksize', default=2048, help='max packet size/default 2048')
@click.option('--mode', default=1, help='set mode=1 (default) redirect, mode=2 zip, mode=3 unzip')
@click.option('--interval', default=0.1, help='actual for mode=2(aggregation/zip) (default) interval=0.1 sec aggregation interval (the packets will be aggregate by time interval or ppm, whats came first)')
@click.option('--ppm', default=10, help='actual for mode=2(aggregation/zip) (default) ppm=10 packets per message (the packets will be aggregate by time interval or ppm, whats came first)')

def main(iprx, iptx, portrx, porttx,mpksize,mode,interval,ppm):

    UDP_IP_RX = iprx
    UDP_PORT_RX = portrx
    
    UDP_IP_TX = iptx
    UDP_PORT_TX = porttx

    MAX_PACKET_SIZE = mpksize
    MODE=mode
    INTR=interval
    PPM=ppm

    def staus_line(pkt,pkts,delay,pksize) -> Table:
        
        table = Table(expand=True,show_header=False,highlight=
                      True,box=box.ASCII2)
        delay=delay*1000
        table.add_column("staus line")
        table.add_row(f"[bold]^X[/] E[yellow]x[/]it pkt:{pkt} pkt/s:{pkts:} delay:{delay:.2f} ms pk_size: [green]{pksize}[/] bytes")
        return table

    def staus_line2(pkt,pkts,delay,pk_min,pk_max) -> Table:

        table = Table(expand=True,show_header=False,highlight=
                      True,box=box.ASCII2)
        delay=delay*1000
        table.add_column("staus line")
        table.add_row(f"[bold]^X[/] E[yellow]x[/]it pkt:{pkt} pkt/s:{pkts:} delay:{delay:.2f} ms pk_size min:[green]{pk_min}[/] max:[green]{pk_max}[/] bytes")
        return table

    #------------------------------------------------------------------
    # Создаем UDP сокет для приема пакетов
    sock_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_rx.bind((UDP_IP_RX, UDP_PORT_RX))
    
    sock_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    console = Console()
    console.print("\n")
    console.rule("UDP-PROXY",style="white") 
    console.print("")
    if MODE==1:
        console.print(f"udp_ip_rx: {UDP_IP_RX} udp_port_rx: {UDP_PORT_RX} udp_ip_tx: {UDP_IP_TX} udp_port_tx: {UDP_PORT_TX} mode: [green]redirect[/]")
    elif MODE==2:
        console.print(f"udp_ip_rx: {UDP_IP_RX} udp_port_rx: {UDP_PORT_RX} udp_ip_tx: {UDP_IP_TX} udp_port_tx: {UDP_PORT_TX} mode: [green]zip[/]")
    elif MODE==2:
        console.print(f"udp_ip_rx: {UDP_IP_RX} udp_port_rx: {UDP_PORT_RX} udp_ip_tx: {UDP_IP_TX} udp_port_tx: {UDP_PORT_TX} mode: [green]unzip[/]")
        
    console.print("")
    console.log("UDP-PROXY started...")
    console.print("")

    i=0
    i_int=0
    time_pp=time.time()
    time_cp=time.time()
    time_int=time.time()
    time_start=time.time()
    pklost=0
    pksize_min=MAX_PACKET_SIZE
    pksize_max=0
    # сохраняем начальные настройки терминала
    old_settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setcbreak(sys.stdin.fileno())  # включаем неканонический режим ввода
        if MODE==1:
            with Live(staus_line(0,0,0,0), refresh_per_second=4) as live:
                pknp=0
                while True:
                    if select.select([sys.stdin], [], [], 0)[0]:  # проверяем, было ли что-то введено
                        c = sys.stdin.read(1)  # читаем символ
                        if c == '\x18':  # проверяем, является ли он CTRL-X
                            live.console.log("UDP-PROXY finished")
                            time_ls=time.time()
                            tt=time_cp-time_start
                            rb=i/(time_ls-time_start)
                            live.console.print()
                            live.console.log("pkt: ",i,"\n")
                            break  # если да, выходим из цикла
                    # Получаем пакет и адрес отправителя
                    packet, addr = sock_rx.recvfrom(MAX_PACKET_SIZE)
                    PACKET_SIZE=len(packet)
                    
                    sock_tx.sendto(packet, (UDP_IP_TX, UDP_PORT_TX))
                    
                    time_cp=time.time()
                    # Извлекаем значения LINK_ID, номера пакета и времени отправки
                    #link_id, packet_number, send_time = struct.unpack("!IId", packet[:16])
                    # Вычисляем задержку между отправкой и получением пакета в микросекундах
                    delay_usec = time_cp-time_pp
                    time_pp=time_cp
                    i+=1
                    # Выводим информацию о полученном пакете и задержке
                    if (time_cp-time_int) >= 1:
                        pkts=i-i_int
                        live.update(staus_line(i,pkts,delay_usec,PACKET_SIZE))
                        i_int=i
                        time_int=time_cp
        elif MODE==2:
            with Live(staus_line2(0,0,0,0,0), refresh_per_second=4) as live:
                    
                while True:
                    if select.select([sys.stdin], [], [], 0)[0]:  # проверяем, было ли что-то введено
                        c = sys.stdin.read(1)  # читаем символ
                        if c == '\x18':  # проверяем, является ли он CTRL-X
                            live.console.log("UDP-RX finished")
                            time_ls=time.time()
                            tt=time_cp-time_start
                            rb=i/(time_ls-time_start)
                            live.console.print()
                            live.console.log("pkt: ",i,"\n")
                            break  # если да, выходим из цикла
                    # Получаем пакет и адрес отправителя
                    packet, addr = sock_rx.recvfrom(MAX_PACKET_SIZE)
                    PACKET_SIZE=len(packet)
                    if PACKET_SIZE <=pksize_min:
                        pksize_min=PACKET_SIZE
                    if PACKET_SIZE>=pksize_max:
                        pksize_max=PACKET_SIZE
                        
                    time_cp=time.time()  
                    link_id=0
                    # Вычисляем задержку между отправкой и получением пакета в микросекундах
                    #delay_usec =(time.time() - send_time)*1000
                    delay_usec = time_cp-time_pp
                    time_pp=time_cp
                    i+=1
                    # Выводим информацию о полученном пакете и задержке                       
                    if (time_cp-time_int) >= 1:
                        pkts=i-i_int
                        live.update(staus_line2(i,pkts,delay_usec,pksize_min,pksize_max))
                        i_int=i
                        time_int=time_cp
        else:
            console.log("[bold red]Error:[/] undefine mode, use --help for more info")
                    
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)  # возвращаем настройки терминала обратно
        
if __name__ == '__main__':
    main()
