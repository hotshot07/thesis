#takes in csv from ./received-csv-files/ 
import time
import os
import queue
from process_csv import process_and_run_prediction
from send_to_db import update_mysql_database

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
    

if __name__ == '__main__':
    try:
        while True:
            new_files = check_new_files('./received_csv_files/')

            if len(new_files)!=0:
                for file in sorted(new_files):
                    if str(file).endswith('.csv'):
                        jobs.put(file)
                        print(f"{file} is in queue")
                    
            time.sleep(2)
            if not jobs.empty():
                unprocessed_path = jobs.get()
                
                predicted_csv_file_path = process_and_run_prediction(unprocessed_path)
                
                #send to mysql database
                try:
                    update_mysql_database(predicted_csv_file_path)
                    os.remove(predicted_csv_file_path)
                except Exception as e:
                    print(e)
                    jobs.put(unprocessed_path)
                         
    except KeyboardInterrupt:
        print("\nQuitting the program.")
    except Exception as e:
        print(e)


    

