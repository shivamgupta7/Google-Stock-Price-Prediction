#Importing modules
import pandas as pd
import json
from datetime import datetime
from kafka import KafkaConsumer
from pyspark.ml.feature import VectorAssembler
from time import sleep

#Declearing consumer connection
try:
    consumer = KafkaConsumer('stock_prices',bootstrap_servers=['localhost:9092'])
except:
    print('connection error')

#getting data and predicting result using the model
def stock_prediction(sqlContext,load_model):
        try:
            for msg in consumer:
                res = json.loads(msg.value.decode('utf-8'))
                dlist = list(res.values())
                pd_df = pd.DataFrame([dlist], columns=['Open', 'Close', 'Volume', 'High', 'Low'])
                pd_df = pd_df.astype(float)
                spark_df = sqlContext.createDataFrame(pd_df)
                vectorAssembler = VectorAssembler(inputCols=['Open', 'High', 'Low'], outputCol='features')
                df_vect = vectorAssembler.transform(spark_df)
                df_vect_features = df_vect.select(['features', 'Close'])
                predictions = load_model.transform(df_vect_features)
                predictions.select("prediction", "Close", "features").show()
                predict_value = predictions.select('prediction').collect()[0].__getitem__("prediction")
                close_value = predictions.select('Close').collect()[0].__getitem__('Close')
                print(msg.key)
                date_time = msg.key.decode('utf-8')
                return round(predict_value, 4), close_value, date_time
        except:
            print('Debug the above lines of code')

