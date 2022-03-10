FROM tensorflow/tensorflow:2.7.1
COPY model_script.py model_server.py process_csv.py send_to_db.py ./
COPY autoencoder_model ./autoencoder_model 
RUN mkdir ./received_csv_files
RUN mkdir ./processed_csvs
RUN apt-get update && apt-get install -y python3 python3-pip vim
RUN pip3 install --upgrade pip
RUN pip3 install Flask numpy pandas keras scikit-learn mysql-connector-python