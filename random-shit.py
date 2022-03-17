from scapy.all import *

pcap = rdpcap('./data/pcaps/wordpress1.pcap')

flags = {
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

i = 0

a = set()

for packet in pcap:
    
    #get flags from the packet 
    # flags = packet.sprintf("%IP.flags%")
    # print(flags)
    i+=1
    
    for x in packet.sprintf('%TCP.flags%'):
        a.add(flags[str(x)])
    # for layer in packet.layers():
    #         packet_layer = packet[layer.__name__]
    #         layer_name = layer.__name__ 
    #         if layer_name == 'TCP':
    #             print(packet_layer.fields.get('flags').flagrepr())
    
print(a)

{'PSH', 'ACK', 'CWR', 'SYN', 'FIN', 'RST', 'UNK', 'ECE'}

