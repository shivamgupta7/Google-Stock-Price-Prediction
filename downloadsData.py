import pandas
import os
from alpha_vantage.timeseries import TimeSeries


def dowload_data(ticker, savefilename):
    '''
    Download stock price data
    '''
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    # print(api_key)
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')
    data.to_csv(savefilename)
    print("Done!")

if __name__ == "__main__":
    dowload_data('GOOGL','google_stock_data.csv')