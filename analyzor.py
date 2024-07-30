
import requests
import datetime
import talib
import pandas as pa
import numpy as np



class data:
    def __init__(self):
        self.price = None
        self.rsi = None


    def Price(self):      
        r = requests.get('https://min-api.cryptocompare.com/data/v2/histohour?fsym=ETH&tsym=USD&limit=50')
        length = len( r.json()['Data']['Data'])-1
        # print('len>>>>>>>>>',len( r.json()['Data']['Data'])-1)
        self.price = r.json()['Data']['Data'][length]['close']
        self.Rsi(r.json())

    def Rsi(self , data):   
        openPrice = []
        closePrice = []

        for i in data['Data']['Data']:
            # print(i)
            openPrice.append(int(i['open']))
            closePrice.append(int(i['close']))
                        
            requiredRsi = pa.DataFrame({'open' : openPrice , 'close' : closePrice})

           

            rr = talib.RSI(requiredRsi['close'])
            rsi = rr.loc[rr.shape[0]-1]
            self.rsi = rsi
            # return (rsi)

    def calculate(self):
        self.Price()
        return ({'price' : self.price , 'rsi' : self.rsi})

