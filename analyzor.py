
import requests
import datetime
import talib
import pandas as pa
import numpy as np
import logging



logging.basicConfig(format='%(asctime)s:%(levelname)s:>>>>>%(message)s', level=logging.DEBUG , datefmt='%m/%d/%Y %I:%M:%S %p')

class data:
    def __init__(self):
        logging.info(' analyzor : i made the instance for the data analyzing...')
        self.price = None
        self.rsi = None


    def Price(self):
        try:
            r = requests.get('https://min-api.cryptocompare.com/data/v2/histohour?fsym=ETH&tsym=USD&limit=50')
            logging.info(' analyzor : i refreshed the price...')
            length = len( r.json()['Data']['Data'])-1
            # print('len>>>>>>>>>',len( r.json()['Data']['Data'])-1)
            self.price = r.json()['Data']['Data'][length]['close']
            logging.info(' analyzor : i give the datas to rsi func for making the rsi data...')
            self.Rsi(r.json())
        except:
            logging.error('someThing went wrong in price func in analyzoe scope...')

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
        logging.info(' analyzor : making the rsi data succeed...')
            # return (rsi)

    def calculate(self):
        logging.info(' analyzor : start the analyze algorithm succeed...')
        self.Price()
        return ({'price' : self.price , 'rsi' : self.rsi})

