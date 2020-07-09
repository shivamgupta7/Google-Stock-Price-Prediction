import pandas
import sys
from alpha_vantage.timeseries import TimeSeries


# Download stock data
ticker = str(sys.argv[1])  # take argument from console
api_key = open('alpha_key.txt').read()

ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')
data.to_csv('google_stock_data.csv')
print("Done!")