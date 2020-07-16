import pandas
import sys
from alpha_vantage.timeseries import TimeSeries


# ticker = str(sys.argv[1])  # take argument from console
def dowload_data(ticker, savefilename):
    '''
    Download stock price data
    '''
    api_key = open('alpha_key.txt').read()
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')
    data.to_csv(savefilename)
    print("Done!")

if __name__ == "__main__":
    dowload_data('GOOGL','google_stock_data.csv')