import mysql.connector

config = {
  'user': 'root',
  'password': 'password',
  'host': 'localhost',
  'port': '52211',
  'database': 'pcap',
  'allow_local_infile':True,
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)

cursor = cnx.cursor()


csv_import = ( f""" 
              LOAD DATA LOCAL INFILE 'converted_file.csv' 
                INTO TABLE pcap_data4
                FIELDS
                TERMINATED BY ','
                ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
              """
              )

cursor.execute(csv_import)

cnx.commit()

cnx.close()

