#takes in csv from ./received-csv-files/ 
import time
import os
import queue
import logging
logging.basicConfig(level=logging.DEBUG)

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
    

try:
    while True:
        new_files = check_new_files('./received_csv_files/')

        if len(new_files)!=0:
            for file in sorted(new_files):
                if str(file).endswith('.csv'):
                    jobs.put(file)
                    logging.debug(f"{file} is in queue")
                    
        time.sleep(2)
        if not jobs.empty():
            unprocessed_path = jobs.get()
            
            logging.debug(f"{unprocessed_path} is being processed")
            predicted_csv_file_path = process_and_run_prediction(unprocessed_path)
            
            logging.debug(f"{predicted_csv_file_path} is being sent to database")
            
            #send to mysql database
            try:
                update_mysql_database(predicted_csv_file_path)
                os.remove(predicted_csv_file_path)
            except Exception as e:
                logging.error(e)
                         
except KeyboardInterrupt:
    logging.debug("\nQuitting the program.")
except Exception as e:
    logging.error(e)


    

