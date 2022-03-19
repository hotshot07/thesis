import pandas as pd 
import numpy as np
from sklearn.preprocessing import Normalizer
from datetime import datetime

hex_lambda = lambda x: int(x,16)

def process_df(unprocessed_df):
    
    final_df = pd.DataFrame()

    list_of_cols_straight = ['length', 'ip.proto', 'ip.len', 'ip.tos',
       'ip.ttl' ,'load.count', 'FIN', 'SYN', 'RST', 'PSH', 'ACK',
       'URG', 'ECE', 'CWR', 'UNK', 'source_docker_bridge', 'source_dns',
       'source_service', 'source_pod', 'source_external',
       'destination_docker_bridge', 'destination_dns', 'destination_service',
       'destination_pod', 'destination_external',
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