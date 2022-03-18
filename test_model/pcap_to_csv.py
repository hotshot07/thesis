import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import os
import csv 

hex_lambda = lambda x: int(x,16)

class Packet():
    packet = None
    
    general_headers = ['length','timestamp']
    eth_headers = ['eth.src','eth.dst','eth.type']
    ip_headers = ['ip.src', 'ip.dst', 'ip.version','ip.proto','ip.len', 'ip.ihl', 'ip.tos', 'ip.ttl']
    raw_headers = ['load.count']
    flags = ['FIN', 'SYN', 'RST', 'PSH', 'ACK', 'URG', 'ECE', 'CWR', 'UNK']
    source_ip_type = ['source_docker_bridge', 'source_dns', 'source_service', 'source_pod', 'source_external']
    destination_ip_type = ['destination_docker_bridge', 'destination_dns', 'destination_service', 'destination_pod', 'destination_external']
    load_bytes = [f'load_{x}' for x in range(20)]

    list_of_headers = general_headers + eth_headers + ip_headers + raw_headers + flags + source_ip_type + destination_ip_type + load_bytes
    
    flag_dict = {
        'F': 'FIN',
        'S': 'SYN',
        'R': 'RST',
        'P': 'PSH',
        'A': 'ACK',
        'U': 'URG',
        'E': 'ECE',
        'C': 'CWR',
        '?': 'UNK'
    }
    
    
    def __init__(self, packet):
        self.packet = packet
        self.packet_dict = {x:0 for x in self.list_of_headers}
        self.extract_data() 
    
    def extract_data(self):
        self.packet_dict['timestamp'] = float(self.packet.time)
        self.packet_dict['length'] = len(self.packet)
        
        for layer in self.packet.layers():
            packet_layer = self.packet[layer.__name__]
            layer_name = layer.__name__ 
            
            if layer_name == 'Ether':
                self.packet_dict['eth.src'] = packet_layer.fields.get('src')
                self.packet_dict['eth.dst'] = packet_layer.fields.get('dst')
                self.packet_dict['eth.type'] = packet_layer.fields.get('type')
                
            if layer_name == 'IP':
                self.packet_dict['ip.src'] = packet_layer.fields.get('src')
                self.check_if_ip_is_internal_or_external(self.packet_dict['ip.src'], kind = 'source')
                self.packet_dict['ip.dst'] = packet_layer.fields.get('dst')
                self.check_if_ip_is_internal_or_external(self.packet_dict['ip.dst'], kind = 'destination')
                
                self.packet_dict['ip.version'] = packet_layer.fields.get('version')
                self.packet_dict['ip.proto'] = packet_layer.fields.get('proto')
                self.packet_dict['ip.len'] = packet_layer.fields.get('len')
                self.packet_dict['ip.ihl'] = packet_layer.fields.get('ihl')
                
                self.packet_dict['ip.tos'] = packet_layer.fields.get('tos')
                self.packet_dict['ip.ttl'] = packet_layer.fields.get('ttl')
            if layer_name == 'TCP':
                self.packet_dict['protocol'] = 'TCP'
                self.packet_dict['protocol.sport'] = packet_layer.fields.get('sport')
                self.packet_dict['protocol.dport'] = packet_layer.fields.get('dport')
                # basically one hot encoding flags here 
                for flg in self.packet.sprintf('%TCP.flags%'):
                    flag_type = self.flag_dict.get(str(flg))
                    self.packet_dict[str(flag_type)] = 1
                
                
            if layer_name == 'Raw':
                self.packet_dict['load.count'] = len(packet_layer.fields.get('load'))
                current_load = str(packet_layer.fields.get('load')[:10].hex())
                
                if current_load != str(0):
                    for i, ch in enumerate(current_load):
                        self.packet_dict[f'load_{i}'] = hex_lambda(ch)
                        
            if layer_name == 'UDP':
                self.packet_dict['protocol'] = 'UDP'
                self.packet_dict['protocol.sport'] = packet_layer.fields.get('sport')
                self.packet_dict['protocol.dport'] = packet_layer.fields.get('dport')
                
        

    def check_if_ip_is_internal_or_external(self,ip, kind = None):
        if not ip:
            return None
        
        split_ip = ip.split('.')
        
        if split_ip[0] == '172' and split_ip[1] == '17':
            self.packet_dict[kind + '_docker_bridge'] = 1
            return
        
        if split_ip[0] == '10' and split_ip[1] == '0' and split_ip[2] == '0' and split_ip[3] == '10':
            self.packet_dict[kind + '_dns'] = 1
            return
        
        if split_ip[0] == '10' and split_ip[1] == '0':
            self.packet_dict[kind + '_service'] = 1
            return
        
        if split_ip[0] == '10' and split_ip[1] == '244':
            self.packet_dict[kind + '_pod'] = 1
            return
        else:
            self.packet_dict[kind + '_external'] = 1
            return 
        
    def return_dict(self):
        return self.packet_dict
    

def convert_pcap_to_csv(path):
    pcap = rdpcap(path)
    
    pcap_dictionary = []

    for packet_var in pcap:
        processed_packet = Packet(packet_var).return_dict()
        if processed_packet.get('protocol') is not None:
            pcap_dictionary.append(processed_packet)
    
        
    head, tail = os.path.split(path)
    
    csv_path = f"{tail.split('.')[0]}.csv"

    with open(csv_path, 'w', newline='') as csv_data_file:
        csv_writer = csv.writer(csv_data_file)
        csv_writer.writerow(pcap_dictionary[0].keys())
        
        for data_row in pcap_dictionary:
            csv_writer.writerow(data_row.values())
    
    return csv_path


if __name__ == '__main__':
    convert_pcap_to_csv('attack1.pcap')