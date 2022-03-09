import mysql.connector
import pandas as pd

config = {
  'user': 'root',
  'password': 'password',
  'host': 'mysql-service',
  'port': '3306',
  'database': 'pcap',
  'allow_local_infile':True,
  'raise_on_warnings': True
}

def update_mysql_database(path_to_processed_csv):

  cnx = mysql.connector.connect(**config)

  cursor = cnx.cursor()

  csv_import = ( f""" 
                LOAD DATA LOCAL INFILE {path_to_processed_csv} 
                  INTO TABLE pcap_table
                  FIELDS
                  TERMINATED BY ','
                  ENCLOSED BY '"'
                  LINES TERMINATED BY '\n'
                """
                )

  cursor.execute(csv_import)

  cnx.commit()

  cnx.close()

