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
    
    #subprocess.call(["ifconfig",wlan,"down"])
    output = subprocess.check_output(["ifconfig",wlan,"down"])
    print(output)

    #subprocess.call(["iw", "dev", wlan, "set", "monitor", "otherbss"])
    output = subprocess.check_output(["iw", "dev", wlan, "set", "monitor", "otherbss"])
    print(output)

    #subprocess.call(["iw","reg","set","BO"])
    output = subprocess.check_output(["iw","reg","set","BO"])
    print(output)

    #subprocess.call(["ifconfig",wlan,"up"])
    output = subprocess.check_output(["ifconfig",wlan,"up"])
    print(output)
    
    output = subprocess.check_output(["iw","dev",wlan,"set","channel",channel,"HT40+"])
    print(output)
    
    wfb_str=""
    print(mode)
    if mode=="rx":
        wfb_str=f"/usr/bin/wfb_rx -p {wfbp} -c {ip} -u {port} -K {key} -i 7669206 {wlan}"
    elif mode=="tx":
        wfb_str=f"/usr/bin/wfb_tx -p {wfbp} -u {port} -K {key} -B 20 -G long -S 1 -L 1 -M 1 -k 8 -n 12 -T 0 -i 7669206 {wlan}"        
    else:
        print("undefine mode value\n useing default params")
        wfb_str=f"/usr/bin/wfb_rx -p {wfbp} -c {ip} -u {port} -K {key} -i 7669206 {wlan}"
    print (wfb_str)
    subprocess.Popen(['xterm', '-e', wfb_str])


if __name__ == '__main__':
    main()
