from scapy.all import *
from scapy.layers.http import *

pcap = rdpcap('./data/pcaps/attack1.pcap')

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

for packet in pcap:

    if packet.haslayer(HTTPRequest)
        print(packet.getlayer(HTTPRequest))
    
    
    
print(a)

# {'PSH', 'ACK', 'CWR', 'SYN', 'FIN', 'RST', 'UNK', 'ECE'}

