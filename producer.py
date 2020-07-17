#Importing necessary modules
from time import sleep
from kafka import KafkaProducer
from alpha_vantage.timeseries import TimeSeries
import os
import json

#Function to get the data from alphavantage
def get_data():
    try:
        ticker = 'GOOGL'
        api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        time = TimeSeries(key=api_key, output_format='json')
        data, metadata = time.get_intraday(symbol=ticker, interval='1min', outputsize='full')
        return data
    except:
        print("Syantax error")

#Function to publish a message
def publish_message(producerkey,key,data_key):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        producerkey.send("stock_prices", json.dumps(data[key]).encode('utf-8'), key_bytes)
        print("message published")
    except:
        print("message not published")

#Function to declear connection to producer
def kafka_producer_connection():
    try:
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        return producer
    except:
        print("Connection error")

#Declearing main function
if __name__=="__main__":
    data = get_data()
    if len(data) > 0:
        kafka_producer = kafka_producer_connection()
        for key in sorted(data):
            publish_message( kafka_producer,key, data[key])
            sleep(3)