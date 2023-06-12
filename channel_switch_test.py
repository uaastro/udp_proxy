import subprocess
import click
import configparser
import select
import time

def main():
    
    wlan='wlx00c0cab1b0be'
    channel_1=161
    channel_2=173
    channel=channel_1
            
    subprocess.run(f"ifconfig {wlan} down",shell=True, check=True)

    subprocess.run(f"iw dev {wlan} set monitor otherbss",shell=True, check=True)

    subprocess.run(f"iw reg set US",shell=True, check=True)

    subprocess.run(f"ifconfig {wlan} up",shell=True, check=True)
            
    i=1
    time_c=time.time()
    time_s=time.time()
    while (time_c-time_s) <= 10:
        if (i%2) == 0:
            channel=channel_2
        else:
            channel=channel_1
                    
        subprocess.run(f"iw dev {wlan} set channel {channel} HT20",shell=True, check=True)
        i+=1
        time_c=time.time()
    print(i)
       

if __name__ == '__main__':
    main()