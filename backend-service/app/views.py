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
    latest_query = """ 
    SELECT *
    FROM pcap_data4
    order by score desc
    limit 100
    """
    
    cursor.execute(latest_query)
    myresult = cursor.fetchall()
    
    cursor.execute("SELECT count(*) FROM pcap_data4")
    analysed_packets = cursor.fetchall()[0]['count(*)']
    
    return render_template("index.html", table_data = myresult, analysed_packets = analysed_packets)

