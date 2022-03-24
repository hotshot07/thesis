FROM ubuntu:18.04
COPY data_server.py ./
RUN mkdir ./received-files
RUN apt-get update && apt-get install -y python3 python3-pip vim
RUN pip3 install --upgrade pip
RUN pip3 install Flask

