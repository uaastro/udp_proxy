#wfb_luncher

import subprocess

wlan="wlx00c0cab1d444"
channel="169"
    
subprocess.run(f"ifconfig {wlan} down",shell=True, check=True)

subprocess.run(f"iw dev {wlan} set monitor otherbss",shell=True, check=True)

subprocess.run(f"iw reg set US",shell=True, check=True)

subprocess.run(f"ifconfig {wlan} up",shell=True, check=True)

subprocess.run(f"iw dev {wlan} set channel {channel} HT20",shell=True, check=True)
