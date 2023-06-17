import configparser
import subprocess
import select

config_file_name='wfb_config_test.ini'

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
                     'ip':'127.0.0.1',
                     'udp_tx_ip':'127.0.0.1',
                     'udp_tx_port':'5602',
                     'udp_tx_pksize':'1024',
                     'udp_tx_pks':'512',
                     'udp_tx_lid':'1',
                     'udp_rx_ip':'127.0.0.1',
                     'udp_rx_port':'5600',
                     'udp_rx_mpksize':'1536',
                     'udp_rx_mode':'2'
                     }


config['wlan_1'] = {'channel': '161',
                    'wlan': 'wlx00c0cab1d444',
                    }

config['tx_video'] = {'tx_key': '/etc/drone.key', #-K
                      'radio_port': '10', #-p
                      'i_link_id': '7669206', #-i
                      'udp_port':'5602'
                      }

config['udp_tx_test'] = {'udp_tx_ip':'127.0.0.1',
                         'udp_tx_port':'5602',
                         'udp_tx_pksize':'1024',
                         'udp_tx_pks':'512'
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


with open(config_file_name, 'w') as configfile:
  config.write(configfile)


config = configparser.ConfigParser()
config.read(config_file_name)
sections = config.sections()
process_list = []

for section in sections:
    
    if section[:4]=='wlan':

        wlans=config[section]['wlan'].split()
        channel=config[section]['channel']
        
        print('wlan: ',wlans)
        print('channel: ',channel)
        
        for wlan in wlans:
        
            print(f'wlan {wlan} setup...')
            print(f"ifconfig {wlan} down")
            print(f"iw dev {wlan} set monitor otherbss")
            print(f"iw reg set US")
            print(f"ifconfig {wlan} up")
            print(f"iw dev {wlan} set channel {channel} HT20")

        
                
    elif section[:2]=='tx':
        options=config[section]
        wfb_xx=["/usr/bin/wfb_tx","-p",options['radio_port'],"-u",options['udp_port'],"-K",options['tx_key'],"-B",options['bandwidth'],"-G",options['G_guard_interval'],"-S",
                options['S_stbc'],"-L",options['L_ldpc'],"-M",options['M_mcs_index'],"-k",options['k_RS_K'],"-n",options['n_RS_N'],"-T",options['T_poll_timeout'],
                "-i",options['i_link_id']]+wlans
        print(wfb_xx)
        
    elif section[:2]=='rx':
        options=config[section]
        wfb_xx=["/usr/bin/wfb_rx","-p",options['radio_port'],"-c",options['ip'],"-u",options['udp_port'],"-K",options['rx_key'],"-i",options['i_link_id']]+wlans
        print(wfb_xx)
    elif section[:6]=='udp_tx':
            options=config[section]
            udp_xx=["/usr/sbin/udp_proxy/udp_tx","--ip",options['udp_tx_ip'],"--port",options['udp_tx_port'],"--pksize",options['udp_tx_pksize'],"--pks",options['udp_tx_pks'],"--lid",options['udp_tx_lid']]
            print(udp_xx)