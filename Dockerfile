FROM debian:latest

RUN apt-get update && apt-get install -y python3 python3-pip
   
COPY requirements.txt /
RUN pip3 install --no-cache-dir -r /requirements.txt

CMD ["python3", "./data/data_analysis.py"]