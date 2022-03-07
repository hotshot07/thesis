from app import app
from flask import url_for,render_template
import mysql.connector

from flask_cors import CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.config['CORS_HEADERS'] = 'Content-Type'

db_config = {
  'user': 'root',
  'password': 'password',
  'host': 'localhost',
  'port': '51280',
  'database': 'pcap',
  'allow_local_infile':True,
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor(dictionary=True)

@app.route("/")
def index():
    queries = """ 
    SELECT *
    FROM pcap_data4
    where score = 2
    limit 20
    """
    
    cursor.execute(queries)
    
    myresult = cursor.fetchall()
    
    return render_template("index.html", table_data = myresult)