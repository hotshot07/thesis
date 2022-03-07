from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import mysql.connector
import json

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

app.config['CORS_HEADERS'] = 'Content-Type'

db_config = {
  'user': 'root',
  'password': 'password',
  'host': 'localhost',
  'port': '52211',
  'database': 'pcap',
  'allow_local_infile':True,
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor(dictionary=True)

@app.route('/', methods=['GET'])
def index():
  queries = """ 
  SELECT *
  FROM pcap_data4
  where score = 2
  limit 5
  """
  
  cursor.execute(queries)
  
  myresult = cursor.fetchall()
  
  return jsonify(myresult)

if __name__ == '__main__':
  app.run(debug=True)
  





cnx.close()