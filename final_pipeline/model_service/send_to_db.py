import mysql.connector
import logging
logging.basicConfig(level=logging.DEBUG)

config = {
  'user': 'root',
  'password': 'password',
  'host': 'localhost',
  'port': '59332',
  'database': 'pcap',
  'allow_local_infile':True,
  'raise_on_warnings': True
}

def update_mysql_database(path_to_processed_csv):

  cnx = mysql.connector.connect(**config)

  cursor = cnx.cursor()
  
  logging.debug(f"Connected to MySQL database, sending {path_to_processed_csv}")
  
  csv_import = ( f"""LOAD DATA LOCAL INFILE '{path_to_processed_csv}'
                  INTO TABLE pcap_table
                  FIELDS 
                    TERMINATED BY ','
                    ENCLOSED BY '"'
                    LINES TERMINATED BY '\n'
                """
                )
  
  cursor.execute(csv_import)
  cnx.commit()
  
  cursor.close()
  cnx.close()
  
if __name__ == '__main__':
  update_mysql_database('./processed_csvs/processed_wordpress1.csv')
