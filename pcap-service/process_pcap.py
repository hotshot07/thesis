import time
import os
import queue
import requests 
from pcap_to_csv import convert_pcap_to_csv

MODEL_SERVICE = 'model-service'
MODEL_PORT = '5000'

DATA_SERVICE = 'data-service'
DATA_PORT = '5000'

jobs = queue.Queue(maxsize=1000)
set_of_files = set()

def check_new_files(path):

    list_of_new_files = []

    for f in os.listdir(path):
        filename = os.path.join(path, f)
        if filename not in set_of_files:
            list_of_new_files.append(filename)
            set_of_files.add(filename)

    return list_of_new_files


def send_file(path, service, port):
    with open(path, "rb") as file:
        file_dict = {'uploaded_file': file}
        try :
            response = requests.post(f"http://{service}:{port}/file", files=file_dict)
            return response.status_code
        except Exception as e:
            print(e) 

if __name__ == '__main__':

    try:
        while True:
            new_files = check_new_files('./received-files/')

            if len(new_files)!=0:
                for file in sorted(new_files):
                    if str(file).endswith('.pcap'):
                        jobs.put(file)
                        print(f"{file} is in queue")
                    
            time.sleep(2)
            if not jobs.empty():
                pcap_path = jobs.get()
                
                #send file to data-service to collect all csv's
                data_service_status_code = send_file(pcap_path, DATA_SERVICE, DATA_PORT)
                
                #send converted 
                converted_csv_path =  convert_pcap_to_csv(pcap_path)
                
                #send file to model-service for processing
                model_service_status_code = send_file(pcap_path, MODEL_SERVICE,MODEL_PORT)
                
                if model_service_status_code == '200' and data_service_status_code == '200':
                    os.remove(pcap_path)
                else:
                    jobs.put(pcap_path)
                
                
    except KeyboardInterrupt:
        print("\nQuitting the program.")
    except Exception as e:
        print(e)


    