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
@click.option('--ip', default="127.0.0.1", help='ip to send packets')
@click.option('--port', default=5602, help='udp port')
@click.option('--pksize', default=1024, help='packet size')
@click.option('--pks', default=800, help='bitrate in pkt/s')
@click.option('--lid', default=1, help='link id')
def main(lid,ip, port,pksize,pks):
    # Адрес и порт для отправки пакетов
    UDP_IP = ip
    UDP_PORT = port
    # Размер пакета в байтах
    PACKET_SIZE = pksize
    # Скорость генерации пакетов в байтах в секунду
    BITRATE = pks  # packets/sec
    link_id = lid
    BASE_DELAY=1/BITRATE

    def staus_line(pkt,pkts) -> Table:
        #table = Table(expand=True,show_header=False,highlight=
        #              True,style="on blue",row_styles=["on blue"],box=None)
        table = Table(expand=True,show_header=False,highlight=
                      True,box=box.ASCII2)
        
        table.add_column("staus line")
        table.add_row(f"[bold]^X[/] E[yellow]x[/]it pkt:{pkt} pkt/s: {pkts:.2f}")
        return table

    #------------------------------------------------------------------
    # Создаем UDP сокет для отправки пакетов
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Оставшиеся байты, заполняемые байтом со значением 255
    remaining_bytes = b"\xFF" * (PACKET_SIZE - 4 - 4 - 8)

    console = Console()

    console.print("\n")
    console.rule("UDP-TX") 
    console.print("")
    console.print(f"link id: {link_id} udp_ip: {UDP_IP} udp_port: {UDP_PORT} pkt size: {PACKET_SIZE} pkt/s: {BITRATE}")
    console.print("")
    console.log("UDP-TX started...")
    console.print("")

    time_ls= time.time()
    time_start= time.time()    
    i=0
    # сохраняем начальные настройки терминала
    old_settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setcbreak(sys.stdin.fileno())  # включаем неканонический режим ввода
        
        with Live(staus_line(0,0), refresh_per_second=4) as live:
                
            while True:
                if select.select([sys.stdin], [], [], 0)[0]:  # проверяем, было ли что-то введено
                    c = sys.stdin.read(1)  # читаем символ
                    if c == '\x18':  # проверяем, является ли он CTRL-X
                        live.console.log("UDP-TX finished")
                        time_ls=time.time()
                        tt=time_ls-time_start
                        rb=i/(time_ls-time_start)
                        live.console.print()
                        live.console.log(f"TX time: {tt:.2f}\n")
                        live.console.log("pkt: ",i,"\n")
                        live.console.log(f"pkt/s: {rb:.2f}\n")
                        break  # если да, выходим из цикла
        
                i+=1
                # Номер пакета (тип uint32)
                packet_number = i
                # Время отправки пакета (тип double)
                packet_time = time.time()
                # Собираем пакет
                packet = struct.pack("!IId"+str((PACKET_SIZE - 4 - 4 - 8))+"s", link_id, packet_number, packet_time,remaining_bytes)
                # Задержка перед отправкой следующего пакета
                delay_usec=BASE_DELAY-(time.time()-time_ls)
                if delay_usec < 0:
                    delay_usec=0
                time.sleep(delay_usec)
                # Отправляем пакет на указанный адрес и порт
                
                sock.sendto(packet, (UDP_IP, UDP_PORT))
                time_ls=time.time() 
                if (i%(BITRATE/4)) == 0:
                    pkts=i/(time_ls-time_start)
                    live.update(staus_line(i,pkts))
                time_ls=time.time()    
                    
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)  # возвращаем настройки терминала обратно
        
if __name__ == '__main__':
    main()
