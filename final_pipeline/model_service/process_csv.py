from uuid import uuid4
import pandas as pd
import numpy as np
from sklearn import metrics
from datetime import datetime
from sklearn.preprocessing import StandardScaler
import keras
import os
import logging

logging.basicConfig(level=logging.DEBUG)

loaded_model = keras.models.load_model("./autoencoder_model")
hex_lambda = lambda x: int(x, 16)

# length,timestamp,ip.src,ip.dst,protocol,protocol.sport,protocol.dport,source_internal,source_external,destination_internal,destination_external
column_order = [
    "uuid",
    "timestamp",
    "length",
    "ip.src",
    "source_internal",
    "source_external",
    "ip.dst",
    "destination_internal",
    "destination_external",
    "protocol",
    "protocol.sport",
    "protocol.dport",
    "score",
]


def process_df(unprocessed_df):

    final_df = pd.DataFrame()

    # IP stuff
    ip_src_list = list(unprocessed_df["ip.src"])

    octet_1_src = []
    octet_2_src = []
    octet_3_src = []
    octet_4_src = []

    for eth in ip_src_list:
        int_ip_list = eth.split(".")
        octet_1_src.append(int_ip_list[0])
        octet_2_src.append(int_ip_list[1])
        octet_3_src.append(int_ip_list[2])
        octet_4_src.append(int_ip_list[3])

    final_df["octet_1_ip_src"] = octet_1_src
    final_df["octet_2_ip_src"] = octet_2_src
    final_df["octet_3_ip_src"] = octet_3_src
    final_df["octet_4_ip_src"] = octet_4_src

    ip_dst_list = list(unprocessed_df["ip.dst"])

    octet_1_dst = []
    octet_2_dst = []
    octet_3_dst = []
    octet_4_dst = []

    for eth in ip_dst_list:
        int_ip_list = eth.split(".")
        octet_1_dst.append(int_ip_list[0])
        octet_2_dst.append(int_ip_list[1])
        octet_3_dst.append(int_ip_list[2])
        octet_4_dst.append(int_ip_list[3])

    final_df["octet_1_ip_dst"] = octet_1_dst
    final_df["octet_2_ip_dst"] = octet_2_dst
    final_df["octet_3_ip_dst"] = octet_3_dst
    final_df["octet_4_ip_dst"] = octet_4_dst

    # columns to get from the csv straight away
    list_of_cols_straight = [
        "length",
        "protocol.sport",
        "protocol.dport",
        "source_internal",
        "source_external",
        "destination_internal",
        "destination_external",
    ]

    for col in list_of_cols_straight:
        final_df[str(col)] = list(unprocessed_df[str(col)])

    dummy_protocol = pd.get_dummies(unprocessed_df["protocol"])
    final_df["TCP"] = list(dummy_protocol["TCP"])
    try:
        final_df["UDP"] = list(dummy_protocol["UDP"])
    except:
        final_df["UDP"] = 0

    # not scaling one hot encoded columns
    columns_not_to_scale = [
        "TCP",
        "UDP",
        "source_internal",
        "source_external",
        "destination_internal",
        "destination_external",
    ]

    time_df = pd.DataFrame(unprocessed_df["timestamp"])

    time_df["packet"] = 1
    time_df["timestamp"] = time_df["timestamp"].apply(
        lambda x: datetime.fromtimestamp(x)
    )
    time_df = time_df.set_index("timestamp")

    time_df = time_df.resample("10s").sum()

    packet_flow_list = []

    for x in list(time_df["packet"]):
        packet_flow_list += [x] * x

    final_df["packet_flow"] = packet_flow_list

    final_df = final_df.astype("float64")

    # Normalizing the data
    # epsilon = 1e-7

    for col in final_df.columns:
        if col not in columns_not_to_scale:
            scale = StandardScaler().fit(final_df[[col]])
            final_df[col] = scale.transform(final_df[[col]])

    data_vector = final_df.values
    pred = loaded_model.predict(data_vector)

    logging.debug("Predictions done")
    return data_vector, pred


def process_and_run_prediction(path_to_csv):
    logging.debug(f"Processing and running prediction for {path_to_csv}")

    unprocessed_df = pd.read_csv(path_to_csv)

    data_vector, predicted_vector = process_df(unprocessed_df)

    uuid_list = [uuid4().hex for _ in range((unprocessed_df.shape[0]))]

    unprocessed_df.insert(0, "uuid", uuid_list)

    score_list = []
    # calculating RMSE score
    for index, x in enumerate(predicted_vector):
        score_list.append(
            np.sqrt(
                metrics.mean_squared_error(predicted_vector[index], data_vector[index])
            )
        )

    unprocessed_df["score"] = score_list

    for col in unprocessed_df.columns:
        if col not in ["timestamp", "score"]:
            unprocessed_df[col] = unprocessed_df[col].apply(str)

    head, tail = os.path.split(path_to_csv)
    processed_path = f"./processed_csvs/processed_{tail}"

    unprocessed_df = unprocessed_df[column_order]

    unprocessed_df.to_csv(processed_path, index=False, header=False, quoting=2)

    return processed_path


if __name__ == "__main__":
    process_and_run_prediction("./received_csv_files/wordpress1.csv")


# final_df looks like
##['octet_1_ip_src', 'octet_2_ip_src', 'octet_3_ip_src', 'octet_4_ip_src',
#    'octet_1_ip_dst', 'octet_2_ip_dst', 'octet_3_ip_dst', 'octet_4_ip_dst',
#    'length', 'protocol.sport', 'protocol.dport', 'source_internal',
#    'source_external', 'destination_internal', 'destination_external',
#    'TCP', 'UDP', 'packet_flow']
