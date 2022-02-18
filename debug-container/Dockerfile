FROM ubuntu:18.04
COPY tcpdump-script.sh polling.py run.sh ./scripts/
RUN mkdir ./scripts/pcap-file
RUN mkdir ./scripts/pcap-to-send
RUN apt-get update && apt-get install -y tcpdump net-tools python3 python3-pip vim
RUN pip3 install requests

