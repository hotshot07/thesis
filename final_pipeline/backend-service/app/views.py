from app import app
from flask import jsonify, url_for,render_template
import mysql.connector

from flask_cors import CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.config['CORS_HEADERS'] = 'Content-Type'

db_config = {
  'user': 'root',
  'password': 'password',
  'host': 'localhost',
  'port': '59332',
  'database': 'pcap',
  'allow_local_infile':True,
  'raise_on_warnings': True
}



@app.route("/")
def index():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor(dictionary=True)
    latest_query = """
    SELECT utctimestamp, packet_length,ip_src, source_internal,source_external,ip_dst,destination_internal,destination_external,protocol,protocol_sport, protocol_dport, score
    FROM pcap_table
    where protocol = 'TCP'
    order by score desc, packet_length desc
    limit 1000
    """
    
    cursor.execute(latest_query)
    myresult = cursor.fetchall()
    
    cursor.execute("SELECT count(*) FROM pcap_table")
    analysed_packets = cursor.fetchall()[0]['count(*)']
    
    
    return render_template("index.html", table_data = myresult, analysed_packets = analysed_packets)
  
@app.route("/interesting_ips")
def interesting_ips():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor(dictionary=True)
    latest_query = """
    Select ip_dst, count(*) as count
    from pcap_table
    where score > 0.5
    group by ip_dst
    order by count desc
    """
    
    cursor.execute(latest_query)
    myresult = cursor.fetchall()
    
    
    return jsonify(myresult)
    # return render_template("index.html", table_data = myresult, analysed_packets = analysed_packets)