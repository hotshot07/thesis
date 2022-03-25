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
    ip_headers = ['ip.src', 'ip.dst']
    protocols = ['protocol', 'protocol.sport', 'protocol.dport']
    
    source_ip_type = ['source_internal', 'source_external']
    destination_ip_type = ['destination_internal', 'destination_external']
    
    list_of_parameters = general_headers + ip_headers + protocols + source_ip_type + destination_ip_type
    
    def __init__(self, packet):
        self.packet = packet
        self.packet_dict = {x:0 for x in self.list_of_parameters}
        self.extract_data() 
    
    def extract_data(self):
        self.packet_dict['timestamp'] = float(self.packet.time)
        self.packet_dict['length'] = len(self.packet)
        
        for layer in self.packet.layers():
            packet_layer = self.packet[layer.__name__]
            layer_name = layer.__name__ 
            
            if layer_name == 'IP':
                self.packet_dict['ip.src'] = packet_layer.fields.get('src')
                self.check_if_ip_is_internal_or_external(self.packet_dict['ip.src'], kind = 'source')
                
                self.packet_dict['ip.dst'] = packet_layer.fields.get('dst')
                self.check_if_ip_is_internal_or_external(self.packet_dict['ip.dst'], kind = 'destination')
    
            if layer_name == 'TCP':
                self.packet_dict['protocol'] = 'TCP'
                self.packet_dict['protocol.sport'] = packet_layer.fields.get('sport')
                self.packet_dict['protocol.dport'] = packet_layer.fields.get('dport')
                
            if layer_name == 'UDP':
                self.packet_dict['protocol'] = 'UDP'
                self.packet_dict['protocol.sport'] = packet_layer.fields.get('sport')
                self.packet_dict['protocol.dport'] = packet_layer.fields.get('dport')

    def check_if_ip_is_internal_or_external(self,ip, kind = None):
        if not ip:
            return None
        
        split_ip = ip.split('.')
        
        if split_ip[0] == '172' and split_ip[1] == '17':
            self.packet_dict[kind + '_internal'] = 1
            return
        
        if split_ip[0] == '10':
            self.packet_dict[kind + '_internal'] = 1
            return
        
        if split_ip[0] == '192' and split_ip[1] == '168':
            self.packet_dict[kind + '_internal'] = 1
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
        if processed_packet.get('protocol') != 0:
            pcap_dictionary.append(processed_packet)
    
        
    head, tail = os.path.split(path)
    
    csv_path = PCAP_CSV_PATH+ f"{tail.split('.')[0]}.csv"

    with open(csv_path, 'w', newline='') as csv_data_file:
        csv_writer = csv.writer(csv_data_file)
        csv_writer.writerow(pcap_dictionary[0].keys())
        
        for data_row in pcap_dictionary:
            csv_writer.writerow(data_row.values())
    
    return csv_path


if __name__ == '__main__':
    convert_pcap_to_csv('./received-files/wordpress1.pcap')