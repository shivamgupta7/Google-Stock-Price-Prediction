import pandas as pd
#Importing linear regression from pyspark mllib
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorAssembler


def data_processing(path):
    '''
    Using Pandas to read data from S3 and return clean dataframe
    '''
    try:
        df = pd.read_csv(path)
    
        df['Date'] = pd.to_datetime(df.date)
        df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
    
        # Renaming columns
        df = df.rename(columns={df.columns[1] : 'Close'})
        df = df.rename(columns={df.columns[3] : 'Open'})
        df = df.rename(columns={df.columns[4] : 'High'})
        df = df.rename(columns={df.columns[5] : 'Low'})
        df = df.rename(columns={df.columns[2] : 'Volume'})
    except:
        print("Given incorrect path")
    return df


def model_training(sqlContext, dataframe, save_path):
    try:
        data = sqlContext.createDataFrame(dataframe)

        # using vector assembler
        featureassembler = VectorAssembler(inputCols=["Open","High","Low"],outputCol="Features")

        output = featureassembler.transform(data)

        finalized_data = output.select("features","Close")

        # spliting the dataset in ratio 8:2 
        train_data, test_data = finalized_data.randomSplit([0.80,0.20])

        #training the model
        lr = LinearRegression(featuresCol='features', labelCol='Close')

        regressor = lr.fit(train_data)

        # training Summary
        trainingSummary=regressor.summary
        rmse = trainingSummary.rootMeanSquaredError
        r2 =  trainingSummary.r2
        #saving the model
        regressor.save(save_path)
        print("\nSuccesfully Saved")
    except:
        print("Model Training is not completed")

    return rmse, r2

