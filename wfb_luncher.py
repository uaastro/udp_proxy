#!/usr/bin/python3

import subprocess
import click
import configparser
import select

@click.command()
@click.option('--conf', default="wfb_config.ini", help='path to config file')

def main(conf):
    
    config = configparser.ConfigParser()
    config.read(conf)
    sections = config.sections()
    process_list = []

    for section in sections:
        
        if section[:4]=='wlan':
    
            wlans=config[section]['wlan'].split()
            channel=config[section]['channel']
            
            for wlan in wlans:
                subprocess.run(f"ifconfig {wlan} down",shell=True, check=True)

                subprocess.run(f"iw dev {wlan} set monitor otherbss",shell=True, check=True)

                subprocess.run(f"iw reg set US",shell=True, check=True)

                subprocess.run(f"ifconfig {wlan} up",shell=True, check=True)

                subprocess.run(f"iw dev {wlan} set channel {channel} HT20",shell=True, check=True)
        
        elif section[:2]=='tx':
            options=config[section]
            wfb_xx=["/usr/bin/wfb_tx","-p",options['radio_port'],"-u",options['udp_port'],"-K",options['tx_key'],"-B",options['bandwidth'],"-G",options['G_guard_interval'],"-S",
                    options['S_stbc'],"-L",options['L_ldpc'],"-M",options['M_mcs_index'],"-k",options['k_RS_K'],"-n",options['n_RS_N'],"-T",options['T_poll_timeout'],
                    "-i",options['i_link_id']] + wlans
            process=subprocess.Popen(wfb_xx, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
            process_list.append(process)
            
        elif section[:2]=='rx':
            options=config[section]
            wfb_xx=["/usr/bin/wfb_rx","-p",options['radio_port'],"-c",options['ip'],"-u",options['udp_port'],"-K",options['rx_key'],"-i",options['i_link_id']]+ wlans
            process=subprocess.Popen(wfb_xx, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
            process_list.append(process)   
    ext=False

    fd_list = [process.stdout.fileno() for process in process_list]

    while ext is False:
        readable, _, _ = select.select(fd_list, [], [])
        for fd in readable:
            for process in process_list:
                if process.stdout.fileno() == fd:
                    output = process.stdout.readline()
                    if output:
                        print(f"[{process.args[0]} {process.args[1]} {process.args[2]}]:", output.strip())



if __name__ == '__main__':
    main()
