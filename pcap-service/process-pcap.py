import time
import os
import queue
from pcaptojson import convert_pcap_to_json

jobs = queue.Queue(maxsize=100)

set_of_files = set()

def check_new_files(path):

    list_of_new_files = []

    for f in os.listdir(path):
        filename = os.path.join(path, f)
        if filename not in set_of_files:
            list_of_new_files.append(filename)
            set_of_files.add(filename)

    return list_of_new_files
    

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
            print(path)
            convert_pcap_to_json(path)
            
except KeyboardInterrupt:
    print("\nQuitting the program.")
except Exception as e:
    print(e)


    