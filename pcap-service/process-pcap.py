import time
import os
import queue
from pcap_to_csv import convert_pcap_to_csv

SERVICE = 'model-service'
PORT = '5000'

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


def send_file(path):
    with open(path, "rb") as file:
        file_dict = {'uploaded_file': file}
        try :
            response = requests.post(f"http://{SERVICE}:{PORT}/file", files=file_dict)
            return response.status_code
        except Exception as e:
            print(e) 

try:
    while True:
        new_files = check_new_files('./received-files/')

        if len(new_files)!=0:
            for file in sorted(new_files):
                if str(file).endswith('.pcap'):
                    jobs.put(file)
                    print(f"{file} is in queue")
                
        time.sleep(5)
        if not jobs.empty():
            path = jobs.get()
            
            #receive path of csv file 
            converted_csv_path =  convert_pcap_to_csv(path)
            
            if str(status_code) == '200':
                os.remove(path)
            else:
                jobs.put(path)
            
            
except KeyboardInterrupt:
    print("\nQuitting the program.")
except Exception as e:
    print(e)


    