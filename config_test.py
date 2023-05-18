import configparser
import subprocess
import select


config = configparser.ConfigParser()
config['DEFAULT'] = {'rx_key': '/etc/rx.key', #-K
                     'tx_key': '/etc/tx.key', #-K
                     'channel': '161',
                     'radio_port': '0', #-p
                     'i_link_id': '7669206', #-i
                     'bandwidth': '20', # -B
                     'wlan': 'waln0',
                     'G_guard_interval': 'long',
                     'S_stbc': '1',
                     'L_ldpc': '1',
                     'M_mcs_index': '1',
                     'k_RS_K': '8',
                     'n_RS_N': '12',
                     'T_poll_timeout': '0',
                     'udp_port':'5600',
                     'ip':'127.0.0.1'
                     }


config['wlan_1'] = {'channel': '161',
                    'wlan': 'wlx00c0cab1d444',
                    }

config['tx_video'] = {'tx_key': '/etc/drone.key', #-K
                      'radio_port': '10', #-p
                      'i_link_id': '7669206', #-i
                      'udp_port':'5602'
                      }

'''
config['rx_video'] = {'rx_key': '/etc/gs.key', #-K
                      'radio_port': '20', #-p
                      'i_link_id': '7669206', #-i
                      'udp_port':'5600'
                      }

config['rx_video_2'] = {'rx_key': '/etc/gs.key', #-K
                      'radio_port': '30', #-p
                      'i_link_id': '7669206', #-i
                      'udp_port':'5601'
                      }

config['wlan_2'] = {'channel': '149',
                    'wlan': 'wlx00c0cab1d777',
                    }

config['tx_video_2'] = {'tx_key': '/etc/drone.key', #-K
                      'radio_port': '40', #-p
                      'i_link_id': '7669444', #-i
                      'udp_port':'5600'
                      }

'''


with open('wfb_config.ini', 'w') as configfile:
  config.write(configfile)


config = configparser.ConfigParser()
config.read('wfb_config.ini')
sections = config.sections()
process_list = []

for section in sections:
    
    if section[:4]=='wlan':

        wlan=config[section]['wlan']
        channel=config[section]['channel']
        '''
        print(f'wlan {wlan} setup...')
        print(f"ifconfig {wlan} down")
        print(f"iw dev {wlan} set monitor otherbss")
        print(f"iw reg set US")
        print(f"ifconfig {wlan} up")
        print(f"iw dev {wlan} set channel {channel} HT20")
        '''
        subprocess.run(f"ifconfig {wlan} down",shell=True, check=True)

        subprocess.run(f"iw dev {wlan} set monitor otherbss",shell=True, check=True)

        subprocess.run(f"iw reg set US",shell=True, check=True)

        subprocess.run(f"ifconfig {wlan} up",shell=True, check=True)

        subprocess.run(f"iw dev {wlan} set channel {channel} HT20",shell=True, check=True)
        
    elif section[:2]=='tx':
        options=config[section]
        wfb_xx=["/usr/bin/wfb_tx","-p",options['radio_port'],"-u",options['udp_port'],"-K",options['tx_key'],"-B",options['bandwidth'],"-G",options['G_guard_interval'],"-S",
                options['S_stbc'],"-L",options['L_ldpc'],"-M",options['M_mcs_index'],"-k",options['k_RS_K'],"-n",options['n_RS_N'],"-T",options['T_poll_timeout'],
                "-i",options['i_link_id'],wlan]
        process=subprocess.Popen(wfb_xx, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
        process_list.append(process)
        
    elif section[:2]=='rx':
        options=config[section]
        wfb_xx=["/usr/bin/wfb_rx","-p",options['radio_port'],"-c",options['ip'],"-u",options['udp_port'],"-K",options['rx_key'],"-i",options['i_link_id'],wlan]
        process=subprocess.Popen(wfb_xx, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
        process_list.append(process)
a=1        
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



