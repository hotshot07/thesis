FROM ubuntu:18.04
COPY . ./service
RUN mkdir ./service/received-files
RUN mkdir ./service/pcap-json
RUN apt-get update && apt-get install -y python3 python3-pip vim
RUN pip3 install --upgrade pip
RUN pip3 install Flask scapy

