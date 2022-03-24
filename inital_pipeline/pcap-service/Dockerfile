FROM ubuntu:18.04
COPY pcap_server.py pcap_to_csv.py process_pcap.py ./
RUN mkdir ./received-files
RUN mkdir ./processed-files
RUN apt-get update && apt-get install -y python3 python3-pip vim
RUN pip3 install --upgrade pip
RUN pip3 install Flask scapy requests 


