from app import app
from flask import url_for,render_template
import mysql.connector

from flask_cors import CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.config['CORS_HEADERS'] = 'Content-Type'

db_config = {
  'user': 'root',
  'password': 'password',
  'host': ' 20.86.233.248',
  'port': '3306',
  'database': 'pcap',
  'allow_local_infile':True,
  'raise_on_warnings': True
}



@app.route("/")
def index():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor(dictionary=True)
    latest_query = """ 
    SELECT utctimestamp, eth_src , eth_dst , packet_length , ip_src, ip_dst, ip_len, ip_ttl, packet_load, load_count, protocol, protocol_sport, protocol_dport, score
    FROM pcap_table
    order by score desc
    limit 1000
    """
    
    cursor.execute(latest_query)
    myresult = cursor.fetchall()
    
    cursor.execute("SELECT count(*) FROM pcap_table")
    analysed_packets = cursor.fetchall()[0]['count(*)']
    
    
    return render_template("index.html", table_data = myresult, analysed_packets = analysed_packets)