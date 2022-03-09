from uuid import uuid4
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import keras



loaded_model = keras.models.load_model("autoencoder_model")
hex_lambda = lambda x: int(x,16)

def process_df(unprocessed_df):
    
    
    unprocessed_df['load'].fillna(0.0, inplace = True)
    unprocessed_df['load.count'].fillna([0]*8, inplace = True)

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

    ip_src_list = list(map(str,list(unprocessed_df['ip.src'])))

    octet_1_src = []
    octet_2_src = []
    octet_3_src = []
    octet_4_src = []

    for eth in ip_src_list:
        int_ip_list = list(eth.split('.'))
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
        int_ip_list = list(eth.split('.'))
        octet_1_dst.append(int_ip_list[0])
        octet_2_dst.append(int_ip_list[1])
        octet_3_dst.append(int_ip_list[2])
        octet_4_dst.append(int_ip_list[3])

    final_df['octet_1_ip_dst'] = octet_1_dst
    final_df['octet_2_ip_dst'] = octet_2_dst
    final_df['octet_3_ip_dst'] = octet_3_dst
    final_df['octet_4_ip_dst'] = octet_4_dst
    
    final_df['ip.len'] = list(unprocessed_df['ip.len'])
    final_df['ip.tos'] = list(unprocessed_df['ip.tos'])
    final_df['ip.ttl'] = list(unprocessed_df['ip.ttl'])
    final_df['length'] = list(unprocessed_df['length'])
    final_df['load.count'] = list(unprocessed_df['load.count'])
    
    dummy_protocol = pd.get_dummies(unprocessed_df['protocol'])
    final_df['TCP'] = list(dummy_protocol['TCP'])
    final_df['UDP'] = list(dummy_protocol['UDP'])
    
    final_df['protocol.dport'] = list(unprocessed_df['protocol.dport'])
    final_df['protocol.sport'] = list(unprocessed_df['protocol.sport'])
    
    final_df = final_df.astype('float64')

    #columns to preprocess (exclude categorial columns like tcp, udp and attack)
    num_cols = ['octet_1_eth_dst', 'octet_2_eth_dst', 'octet_3_eth_dst',
        'octet_4_eth_dst', 'octet_5_eth_dst', 'octet_6_eth_dst',
        'octet_1_eth_src', 'octet_2_eth_src', 'octet_3_eth_src',
        'octet_4_eth_src', 'octet_5_eth_src', 'octet_6_eth_src',
        'octet_1_ip_dst', 'octet_2_ip_dst', 'octet_3_ip_dst', 'octet_4_ip_dst',
        'ip.len', 'ip.tos', 'ip.ttl', 'length', 'load.count',
        'protocol.dport', 'protocol.sport']

    for i in num_cols:
        scale = StandardScaler().fit(final_df[[i]])
        final_df[i] = scale.transform(final_df[[i]])
        
    
    data_vector = final_df.values
    pred = model.predict(data_vector)
    
    score_list = []
    for index, x in enumerate(pred):
        score_list.append(np.sqrt(metrics.mean_squared_error(pred[index],data_vector[index])))
    
    return pred
    
    #returns model_predict values

process_and_run_prediction(path_to_csv):
    unprocessed_csv = pd.read_csv(path_to_csv)
    
    predicted_vector = process_df(unprocessed_csv)

    uuid_list = [uuid4().hex for i in range(len(unprocessed_csv.shape[0]))]
    
    unprocessed_csv.insert(0, 'uuid', uuid_list)
    
    score_list = []
    for index, x in enumerate(pred):
        score_list.append(np.sqrt(metrics.mean_squared_error(pred[index],x_normal[index])))
    unprocessed_csv["score"] = score_list
    
    for col in unprocessed_csv.columns:
        if col not in ['timestamp','score']
            unprocessed_csv[col] = unprocessed_csv[col].apply(str)
    
    head, tail = os.path.split(path_to_csv)
    processed_path = f'./processed_csvs/processed_{tail}'
    unprocessed_csv.to_csv(processed_path,index = False, header = False, quoting=2)

    return processed_path


def check_if_ip_is_internal_or_external(ip):
    
    split_ip = ip.split('.')
    
    print(split_ip)
    if split_ip[0] == '172' and split_ip[1] == '17':
        return 'docker_bridge'
    
    if split_ip[0] == '10' and split_ip[1] == '0' and split_ip[2] == '0' and split_ip[3] == '10':
        return 'dns'
    
    if split_ip[0] == '10' and split_ip[1] == '0':
        return 'service'
    
    if split_ip[0] == '10' and split_ip[1] == '244':
        return 'pod'
    
    else:
        return 'external' 
    
    
if __name__ == '__main__':
    process_and_run_prediction()