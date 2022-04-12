import pandas as pd 
import numpy as np
from sklearn.preprocessing import Normalizer


hex_lambda = lambda x: int(x,16)

def process_df(unprocessed_df):
    
    final_df = pd.DataFrame()

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
    
    final_df = final_df.astype('float64')
    
    for col in final_df:
        if col not in columns_not_to_scale:
            #normalize
            maxi = float(final_df[col].max())
            mini = float(final_df[col].min())
            sub = maxi - mini
            final_df[col] = final_df[col].apply(lambda x: (float(x) - mini)/sub)
    
    return final_df 