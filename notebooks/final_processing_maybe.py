#with standard scalar
import pandas as pd 
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from datetime import datetime

hex_lambda = lambda x: int(x,16)

def process_df(unprocessed_df):
    
    final_df = pd.DataFrame()

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

    list_of_cols_straight = ['length','protocol.sport', 'protocol.dport', 'source_pod',
           'source_external', 'destination_pod', 'destination_external']

    for col in list_of_cols_straight:
        final_df[str(col)] = list(unprocessed_df[str(col)])

    dummy_protocol = pd.get_dummies(unprocessed_df['protocol'])
    final_df['TCP'] = list(dummy_protocol['TCP'])
    try:
        final_df['UDP'] = list(dummy_protocol['UDP'])
    except:
        final_df['UDP'] = 0
    
    columns_not_to_scale = ['source_docker_bridge', 'source_dns', 'source_service', 'destination_docker_bridge', 'destination_dns',
           'destination_service', 'destination_pod', 'destination_external', 'TCP', 'UDP', 'source_pod','source_external']
    
    
    ### much better logic for time
    
    unprocessed_df['timestamp'] = unprocessed_df['timestamp'].apply(lambda x: int(x))
    
    min_timestamp = unprocessed_df['timestamp'].min()
    max_timestamp = unprocessed_df['timestamp'].max()
    
    total_packet_list = []

    for ts in range(min_timestamp, max_timestamp , 10):
        
        interval = 9
        if ts + interval > max_timestamp:
            interval = max_timestamp - ts
        
        time_df = unprocessed_df[unprocessed_df['timestamp'].between(ts, ts+interval)].copy()
        
        ip_value_count_dict = time_df['ip.dst'].value_counts().to_dict()
        
        time_df['packet_flow_10_s'] = time_df['ip.dst'].apply(lambda x: ip_value_count_dict[str(x)])

        for x in list(time_df['packet_flow_10_s']):
            total_packet_list.append(x)
    
    final_df['packet_flow_10_s'] = total_packet_list
    
    
    
    
    # time_df = pd.DataFrame(unprocessed_df['timestamp'])
    
    # time_df['packet'] = 1
    # time_df['timestamp'] = time_df['timestamp'].apply(lambda x: datetime.fromtimestamp(x))
    # time_df = time_df.set_index('timestamp')
    
    # time_df = time_df.resample('10s').sum()
    
    # packet_flow_list = []
    
    # for x in list(time_df['packet']):
    #     packet_flow_list += [x]*x 
    
    # final_df['packet_flow'] = packet_flow_list
    
    
    final_df = final_df.astype('float64')
    
    
    #Normailizing the data
    # epsilon = 1e-7
    
    for col in final_df.columns:
        if col not in columns_not_to_scale:
            scale = StandardScaler().fit(final_df[[col]])
            final_df[col] = scale.transform(final_df[[col]])
            
    return final_df 