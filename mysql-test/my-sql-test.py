import mysql.connector

config = {
  'user': 'root',
  'password': 'password',
  'host': 'localhost',
  'port': '58074',
  'database': 'pcap',
  'allow_local_infile':True,
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)

cursor = cnx.cursor()

damn = "dam.csv"

csv_import = ( f""" 
              LOAD DATA LOCAL INFILE '{damn}' 
                INTO TABLE Persons
                FIELDS
                TERMINATED BY ','
                ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
              """
              )

cursor.execute(csv_import)

# Make sure data is committed to the database
cnx.commit()

cnx.close()

