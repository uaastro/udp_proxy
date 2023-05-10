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
@click.option('--ip', default="127.0.0.1", help='address of udp server/default 127.0.0.1')
@click.option('--port', default=5600, help='port of udp server/default 5600')
@click.option('--mpksize', default=1024, help='max packet size/default 1024')
@click.option('--mode', default=1, help='set mode=1 (default) for accept udp_test packets generated by ud_tx or set mode=2 for any other udp packets format')

def main(ip, port,mpksize,mode):
    # Адрес и порт для отправки пакетов
    UDP_IP = ip
    UDP_PORT = port
    # Размер пакета в байтах
    MAX_PACKET_SIZE = mpksize
    MODE=mode
    

    def staus_line(link_id,pkt,pkts,delay,pksize,pk_lost) -> Table:
        #table = Table(expand=True,show_header=False,highlight=
        #              True,style="on blue",row_styles=["on blue"],box=None)
        table = Table(expand=True,show_header=False,highlight=
                      True,box=box.ASCII2)
        delay=delay*1000
        table.add_column("staus line")
        table.add_row(f"[bold]^X[/] E[yellow]x[/]it link_id:{link_id} pkt:{pkt} pkt/s:{pkts:} delay:{delay:.2f} ms pk_size: [green]{pksize}[/] bytes pk_lost:{pk_lost}")
        return table

    def staus_line2(pkt,pkts,delay,pk_min,pk_max,apkt_size) -> Table:
        #table = Table(expand=True,show_header=False,highlight=
        #              True,style="on blue",row_styles=["on blue"],box=None)
        table = Table(expand=True,show_header=False,highlight=
                      True,box=box.ASCII2)
        delay=delay*1000
        table.add_column("staus line")
        table.add_row(f"[bold]^X[/] E[yellow]x[/]it pkt:{pkt} pkt/s:{pkts:} delay:{delay:.2f} ms pk_size min:[green]{pk_min}[/] max:[green]{pk_max}[/] avg:[green]{apkt_size}[/] bytes")
        return table

    #------------------------------------------------------------------
    # Создаем UDP сокет для приема пакетов
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    console = Console()
    console.print("\n")
    console.rule("UDP-RX",style="blue") 
    console.print("")
    if MODE==1:
        console.print(f"udp_ip: {UDP_IP} udp_port: {UDP_PORT} mode: [green]test[/]")
    elif MODE==2:
        console.print(f"udp_ip: {UDP_IP} udp_port: {UDP_PORT} mode: [green]discovery[/]")
    console.print("")
    console.log("UDP-RX started...")
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
            with Live(staus_line(0,0,0,0,0,0), refresh_per_second=4) as live:
                pknp=0
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
                    packet, addr = sock.recvfrom(MAX_PACKET_SIZE)
                    PACKET_SIZE=len(packet)
                    time_cp=time.time()
                    # Извлекаем значения LINK_ID, номера пакета и времени отправки
                    link_id, packet_number, send_time = struct.unpack("!IId", packet[:16])
                    # Вычисляем задержку между отправкой и получением пакета в микросекундах
                    delay_usec = time_cp-time_pp
                    time_pp=time_cp
                    i+=1
                    # Выводим информацию о полученном пакете и задержке
                    #pkts=0
                    if pknp==0:
                        pknp=packet_number
                    else:
                        if (packet_number-pknp)>1:
                            pklost+=packet_number-pknp-1
                            pknp=packet_number
                        else:
                            pknp=packet_number
                    if (time_cp-time_int) >= 1:
                        pkts=i-i_int
                        live.update(staus_line(link_id,i,pkts,delay_usec,PACKET_SIZE,pklost))
                        i_int=i
                        time_int=time_cp
        elif MODE==2:
            with Live(staus_line2(0,0,0,0,0,0), refresh_per_second=4) as live:
                stream_size=0
                apkt_size=0
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
                            live.console.log("",)
                            break  # если да, выходим из цикла
                    # Получаем пакет и адрес отправителя
                    packet, addr = sock.recvfrom(MAX_PACKET_SIZE)
                    PACKET_SIZE=len(packet)
                    
                    stream_size+=PACKET_SIZE
                    apkt_size=stream_size/i
                    
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
                        live.update(staus_line2(i,pkts,delay_usec,pksize_min,pksize_max,apk_size))
                        i_int=i
                        time_int=time_cp
        else:
            console.log("[bold red]Error:[/] undefine mode, use --help for more info")
                    
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)  # возвращаем настройки терминала обратно
        
if __name__ == '__main__':
    main()
