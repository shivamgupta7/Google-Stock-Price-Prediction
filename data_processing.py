import boto3
import pandas as pd

def data_processing(path):
    '''
    Using Pandas to read data from S3 and return clean dataframe
    '''
    try:
        df = pd.read_csv(path)
        print("After reading data from S3: \n",df.head())

        # # EXPLORATORY DATA ANALYSIS
        print("\nCount of each column : \n", df.count())
        print("\nData type of each column : \n", df.dtypes)
        print("\nData Information : ",df.info())
        df['Date'] = pd.to_datetime(df.date)
        df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
        print(df['Date'])

        print(df.columns.tolist())

        # Renaming columns
        df = df.rename(columns={df.columns[1] : 'Close'})
        df = df.rename(columns={df.columns[3] : 'Open'})
        df = df.rename(columns={df.columns[4] : 'High'})
        df = df.rename(columns={df.columns[5] : 'Low'})
        df = df.rename(columns={df.columns[2] : 'Volume'})

        # printing top  5 rows
        print(df.head())
        # Discriptive statistics of dataset 
        print("\nDataset Statistics : \n", df.describe())

        # Checking null values
        print("\nCheck Null value of each columns : \n",df.isnull().sum())
        #finding correlation function
        print("\nCorrelation between each feature : \n",df.corr())
    except PermissionError:
        print("File path not found", path)

def main():
    #creating client obj for s3
    boto3.client('s3')
    path = 's3://googlestockdata/data/google_stock_data.csv'
    data_processing(path)

if __name__ == "__main__":
    main()