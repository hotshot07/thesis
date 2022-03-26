import pandas as pd 
import numpy as np

hex_lambda = lambda x: int(x,16)

def process_df(unprocessed_df):
    
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
    
    return final_df 


def check_if_ip_is_internal_or_external(ip: str) -> str:
    
    split_ip = ip.split('.')
    
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