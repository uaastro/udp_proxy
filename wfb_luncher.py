#wfb_luncher

import subprocess
import click


@click.command()
@click.option('--key', default="/etc/gs.key", help='key (gs.key or drone.key) file default /etc/gs.key')
@click.option('--mode', default="rx", help='tx/rx mode default rx')
@click.option('--port', default="5600", help='port of udp outgoing/lossening default 5600')
@click.option('--wlan', default="wl0", help='wlan adapter default wl0')
@click.option('--channel', default="161", help='wlan adapter default wl0')
@click.option('--ip', default="127.0.0.1", help='ip adress of source/destination default 127.0.0.1')
@click.option('--wfbp', default="0", help='id of wfb pipe default 0')

def main(key,mode,port,wlan,channel,ip,wfbp):
    
    subprocess.run(f"ifconfig {wlan} down",shell=True, check=True)

    subprocess.run(f"iw dev {wlan} set monitor otherbss",shell=True, check=True)

    subprocess.run(f"iw reg set US",shell=True, check=True)

    subprocess.run(f"ifconfig {wlan} up",shell=True, check=True)

    subprocess.run(f"iw dev {wlan} set channel {channel} HT20",shell=True, check=True)
    
    if mode=="rx":
        wfb_xx=["/usr/bin/wfb_rx","-p",wfbp,"-c",ip,"-u",port,"-K",key,"-i","7669206",wlan]
    elif mode=="tx":
        wfb_xx=["/usr/bin/wfb_tx","-p",wfbp,"-u",port,"-K",key,"-B","20","-G","long","-S","1","-L","1","-M","1","-k","8","-n","12","-T","0","-i","7669206",wlan]        
    else:
        print("undefine mode value\n useing default params")
        wfb_xx=["/usr/bin/wfb_rx","-p",wfbp,"-c",ip,"-u",port,"-K",key,"-i","7669206",wlan]
        
    with subprocess.Popen(wfb_xx, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as proc:
            
        while proc.poll() is None:
            for line in proc.stdout:
                print(line, end='')
        print(proc.returncode)


if __name__ == '__main__':
    main()
