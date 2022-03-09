import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import json 
import os
import csv 

PCAP_CSV_PATH = './processed-files/'


class Packet():
    packet = None
    general_headers = ['length','timestamp']
    eth_headers = ['eth.src','eth.dst','eth.type']
    ip_headers = ['ip.src', 'ip.dst', 'ip.version','ip.proto','ip.len', 'ip.ihl', 'ip.tos', 'ip.flags', 'ip.ttl']
    # tcp_headers = ['tcp.sport', 'tcp.dport' ,'tcp.reserved' ,'tcp.flags', 'tcp.urgptr']
    raw_headers = ['load', 'load.count']
    # udp_headers = ['udp.sport', 'udp.dport', 'udp.len']
    list_of_headers = general_headers + eth_headers + ip_headers + raw_headers 
    
    def __init__(self, packet):
        self.packet = packet
        self.packet_dict = {x:None for x in self.list_of_headers}
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
                self.packet_dict['ip.dst'] = packet_layer.fields.get('dst')
                self.packet_dict['ip.version'] = packet_layer.fields.get('version')
                
                self.packet_dict['ip.proto'] = packet_layer.fields.get('proto')
                self.packet_dict['ip.len'] = packet_layer.fields.get('len')
                self.packet_dict['ip.ihl'] = packet_layer.fields.get('ihl')
                
                self.packet_dict['ip.tos'] = packet_layer.fields.get('tos')
                self.packet_dict['ip.flags'] = packet_layer.fields.get('flags').flagrepr()
                self.packet_dict['ip.ttl'] = packet_layer.fields.get('ttl')
            if layer_name == 'TCP':
                self.packet_dict['protocol'] = 'TCP'
                self.packet_dict['protocol.sport'] = packet_layer.fields.get('sport')
                self.packet_dict['protocol.dport'] = packet_layer.fields.get('dport')
                
            if layer_name == 'Raw':
                self.packet_dict['load.count'] = len(packet_layer.fields.get('load'))
                self.packet_dict['load'] = packet_layer.fields.get('load')[:8].hex(' ')
            if layer_name == 'UDP':
                self.packet_dict['protocol'] = 'UDP'
                self.packet_dict['protocol.sport'] = packet_layer.fields.get('sport')
                self.packet_dict['protocol.dport'] = packet_layer.fields.get('dport')

        
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
    
    csv_path = PCAP_CSV_PATH+ f"{tail.split('.')[0]}.csv"

    with open(csv_path, 'w', newline='') as csv_data_file:
        csv_writer = csv.writer(csv_data_file)
        csv_writer.writerow(pcap_dictionary[0].keys())
        
        for data_row in pcap_dictionary:
            csv_writer.writerow(data_row.values())
    
    return csv_path
