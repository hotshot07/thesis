import time
import os
import queue
import requests

jobs = queue.Queue(maxsize=1000)

env_dict = os.environ

SERVICE = env_dict["PCAP_INTERNAL_SERVICE_SERVICE_HOST"]
PORT = env_dict["PCAP_INTERNAL_SERVICE_SERVICE_PORT"]

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
    try:
        with open(path, "rb") as file:
            file_dict = {"uploaded_file": file}
            try:
                response = requests.post(
                    f"http://{SERVICE}:{PORT}/file", 
                    files=file_dict
                )
                return response.status_code
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


while True:
    new_files = check_new_files("pcap-to-send/")

    if len(new_files) != 0:
        for file in sorted(new_files):
            if str(file).endswith(".pcap"):
                jobs.put(file)
                print(f"{file} is in queue")

    time.sleep(5)
    if not jobs.empty():
        path = jobs.get()
        status_code = send_file(path)
        if str(status_code) == "200":
            print(f"{path} is being sent to pcap-service")
            os.remove(path)
        else:
            jobs.put(path)
            print(f"{path} is being re-added to queue")
