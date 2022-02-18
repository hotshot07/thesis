from scapy.all import *
import json 
import os 


PCAP_JSON_PATH = './pcap-json/'

def set_default(obj):
        if isinstance(obj, set):
            return list(obj)

def convert_pcap_to_json(path):
    pcap = rdpcap(path)
    
    pcap_dictionary = {}

    for packet in pcap:
        
        layer_names = [layer.__name__ for layer in packet.layers()]
    
        packet_dict = {layer : packet.getlayer(layer).fields for layer in layer_names}
        
        pcap_dictionary[str(packet.time)] = packet_dict
    
    head, tail = os.path.split(path)
    
        
    with open(PCAP_JSON_PATH + f"pcap-{tail.split('.')[0]}.json", 'w') as fp:
        json.dump(pcap_dictionary, fp, default=set_default, sort_keys= True, indent= 4)
        

# if __name__ == '__main__':
#     convert_pcap_to_json('/Users/hotshot07/Desktop/pack-analyser/azure.pcap')
    