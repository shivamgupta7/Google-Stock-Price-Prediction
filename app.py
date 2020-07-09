import boto3
import time
import json
from consumer import stock_prediction
from datetime import datetime
from flask import Flask, render_template,make_response
#Importing spark modules
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.regression import LinearRegressionModel
from trainingModel import data_processing, model_training

boto3.client('s3')
sc = SparkContext()
sqlContext = SQLContext(sc)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('stockgraph.html')

#Declearing the data path
data_path = "s3://googlestockdata/data/google_stock_data.csv"

@app.route('/model-train')
def train():
    try:
        df = data_processing(data_path)
        rmse, r2 = model_training(sqlContext, df)
        return render_template('modeltraining.html',rmse_error=rmse, r2_error=r2)
    except:
        print('Path is not found')


#Declearing the model path
try:
    Path = "file:/home/hadoopuser/Documents/Google-Stock-Price-Prediction/Stock_Model"
    load_model = LinearRegressionModel.load(Path)
except:
    print("Decleared wrong path")


@app.route('/data')
def data():
    try:
        pred_price, actual_price, date_time = stock_prediction(sqlContext, load_model)
        date_time = int(datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').strftime('%s'))* 1000
        data = [date_time, pred_price, actual_price]
        response= make_response(json.dumps(data))
        response.content_type = 'application/json'
        time.sleep(2)
        return response
    except:
        print("response was not sucessfull")


if __name__== "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000, passthrough_errors=True)