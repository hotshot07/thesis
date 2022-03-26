import pandas as pd 
import numpy as np
from sklearn.preprocessing import Normalizer
from datetime import datetime

hex_lambda = lambda x: int(x,16)

def process_df(unprocessed_df):
    
    final_df = pd.DataFrame()
    
    #creates final_df and starts updating the final_df
    eth_dst_list = list(unprocessed_df['eth.dst'])

    octet_1_dst = []
    octet_2_dst = []
    octet_3_dst = []
    octet_4_dst = []
    octet_5_dst = []
    octet_6_dst = []

    for eth in eth_dst_list:
        int_eth_list = list(map(hex_lambda, eth.split(':')))
        octet_1_dst.append(int_eth_list[0])
        octet_2_dst.append(int_eth_list[1])
        octet_3_dst.append(int_eth_list[2])
        octet_4_dst.append(int_eth_list[3])
        octet_5_dst.append(int_eth_list[4])
        octet_6_dst.append(int_eth_list[5])

    # creating a final dataframe that will be used to store modified data
    final_df = pd.DataFrame(octet_1_dst, columns =['octet_1_eth_dst'])
    final_df['octet_2_eth_dst'] = octet_2_dst
    final_df['octet_3_eth_dst'] = octet_3_dst
    final_df['octet_4_eth_dst'] = octet_4_dst
    final_df['octet_5_eth_dst'] = octet_5_dst
    final_df['octet_6_eth_dst'] = octet_6_dst
    
    ##eth_src
    eth_src_list = list( unprocessed_df['eth.src'])

    octet_1_src = []
    octet_2_src = []
    octet_3_src = []
    octet_4_src = []
    octet_5_src = []
    octet_6_src = []

    for eth in eth_src_list:
        int_eth_list = list(map(hex_lambda, eth.split(':')))
        octet_1_src.append(int_eth_list[0])
        octet_2_src.append(int_eth_list[1])
        octet_3_src.append(int_eth_list[2])
        octet_4_src.append(int_eth_list[3])
        octet_5_src.append(int_eth_list[4])
        octet_6_src.append(int_eth_list[5])
        
    final_df['octet_1_eth_src'] = octet_1_src 
    final_df['octet_2_eth_src'] = octet_2_src
    final_df['octet_3_eth_src'] = octet_3_src
    final_df['octet_4_eth_src'] = octet_4_src
    final_df['octet_5_eth_src'] = octet_5_src
    final_df['octet_6_eth_src'] = octet_6_src

    ip_src_list = list(unprocessed_df['ip.src'])

    octet_1_src = []
    octet_2_src = []
    octet_3_src = []
    octet_4_src = []

    for eth in ip_src_list:
        int_ip_list = eth.split('.')
        octet_1_src.append(int_ip_list[0])
        octet_2_src.append(int_ip_list[1])
        octet_3_src.append(int_ip_list[2])
        octet_4_src.append(int_ip_list[3])

    final_df['octet_1_ip_src'] = octet_1_src 
    final_df['octet_2_ip_src'] = octet_2_src
    final_df['octet_3_ip_src'] = octet_3_src
    final_df['octet_4_ip_src'] = octet_4_src
    
    
    ip_dst_list = list(unprocessed_df['ip.dst'])

    octet_1_dst = []
    octet_2_dst = []
    octet_3_dst = []
    octet_4_dst = []

    for eth in ip_dst_list:
        int_ip_list = eth.split('.')
        octet_1_dst.append(int_ip_list[0])
        octet_2_dst.append(int_ip_list[1])
        octet_3_dst.append(int_ip_list[2])
        octet_4_dst.append(int_ip_list[3])

    final_df['octet_1_ip_dst'] = octet_1_dst
    final_df['octet_2_ip_dst'] = octet_2_dst
    final_df['octet_3_ip_dst'] = octet_3_dst
    final_df['octet_4_ip_dst'] = octet_4_dst

    list_of_cols_straight = ['length', 'ip.proto', 'ip.len', 'ip.tos',
       'ip.ttl' ,'load.count', 'FIN', 'SYN', 'RST', 'PSH', 'ACK',
       'URG', 'ECE', 'CWR', 'UNK', 'source_docker_bridge', 'source_dns',
       'source_service', 'source_pod', 'source_external',
       'destination_docker_bridge', 'destination_dns', 'destination_service',
       'destination_pod', 'destination_external', 'load_0', 'load_1', 'load_2',
       'load_3', 'load_4', 'load_5', 'load_6', 'load_7', 'load_8', 'load_9',
       'load_10', 'load_11', 'load_12', 'load_13', 'load_14', 'load_15',
       'load_16', 'load_17', 'load_18', 'load_19',
       'protocol.sport', 'protocol.dport']

    for col in list_of_cols_straight:
        final_df[str(col)] = list(unprocessed_df[str(col)])

    dummy_protocol = pd.get_dummies(unprocessed_df['protocol'])
    final_df['TCP'] = list(dummy_protocol['TCP'])
    final_df['UDP'] = list(dummy_protocol['UDP'])
    
    columns_not_to_scale = ['FIN', 'SYN', 'RST', 'PSH', 'ACK', 'URG', 'ECE', 'CWR', 'UNK',
           'source_docker_bridge', 'source_dns', 'source_service', 'source_pod',
           'source_external', 'destination_docker_bridge', 'destination_dns',
           'destination_service', 'destination_pod', 'destination_external', 'TCP',
           'UDP']
    
    time_df = pd.DataFrame(unprocessed_df['timestamp'])
    
    time_df['packet'] = 1
    time_df['timestamp'] = time_df['timestamp'].apply(lambda x: datetime.fromtimestamp(x))
    time_df = time_df.set_index('timestamp')
    
    time_df = time_df.resample('10s').sum()
    
    packet_flow_list = []
    
    for x in list(time_df['packet']):
        packet_flow_list += [x]*x 
    
    final_df['packet_flow'] = packet_flow_list
    
    
    final_df = final_df.astype('float64')
    
    
    #Normailizing the data
    
    for col in final_df:
        if col not in columns_not_to_scale:
            #normalize
            maxi = float(final_df[col].max())
            mini = float(final_df[col].min())
            sub = maxi - mini
            final_df[col] = final_df[col].apply(lambda x: (float(x) - mini)/sub)
            
    return final_df 