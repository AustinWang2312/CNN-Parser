from alpha_vantage.timeseries import TimeSeries
import matplotlib.ticker as mticker
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
# pylint: disable=E1101
class Stock:
    def __init__(self,sym):
        self.sym=sym

    def time_series_intraday(self):
        ts = TimeSeries(key='3YHL8BR00PZ5L9JA',output_format='pandas')
        data ,meta_data= ts.get_intraday(symbol=self.sym,interval='1min', outputsize='full')
        return data

class Visualizer:
    def __init__(self,stock):
        self.stock=stock
        self.data=self.stock.time_series_intraday()
        
    def graph(self,date):
        self.data=self.data[:date]
        self.data['4. close'].plot()
        plt.title(self.stock.sym+" Intraday Time Series")
        plt.show()


#x=Stock("TSLA")
#y=Visualizer(x)
#y.graph('2010-07-10 04:22:00')
