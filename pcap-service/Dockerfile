FROM ubuntu:18.04
COPY basic-server.py pcaptojson.py process-pcap.py ./service/
RUN mkdir ./service/received-files
RUN mkdir ./service/pcap-json
RUN apt-get update && apt-get install -y python3 python3-pip vim
RUN pip3 install --upgrade pip
RUN pip3 install Flask scapy

