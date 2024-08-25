

import requests
import datetime
import talib
import pandas as pa
import numpy as np
import logging
import pytz
#import spider
#from spider import run_client as message
import socketio
import psutil
IP=[(k, addr.address) for k, v in psutil.net_if_addrs().items() for addr in v if addr.family == -1]
print(len(IP))
sio = socketio.SimpleClient()
sio.connect('https://test.spider-cryptobot.site', namespaces='/analyzor' ,headers = {'MACAddress' : IP[len(IP)-1][1]})


def run_client(msg):
    sio.emit('new message', {'data' : msg})


def getTime():
    zone = pytz.timezone("America/New_York")
    return {'hour' : int(datetime.datetime.now(zone).hour) , 'minute' : int(datetime.datetime.now(zone).minute) }

logging.basicConfig(format='%(asctime)s:%(levelname)s:>>>>>%(message)s', level=logging.DEBUG , datefmt='%m/%d/%Y %I:%M:%S %p')

class data:
    def __init__(self):
        logging.info(' analyzor : i made the instance for the data analyzing...')
        run_client(f'>>>analyzor : i will make the data for analyzing... => time :: {getTime()["hour"]}:{getTime()["minute"]}')
        self.price = None
        self.rsi = None


    def Price(self):
        try:
            r = requests.get('https://min-api.cryptocompare.com/data/v2/histohour?fsym=ETH&tsym=USD&limit=50')
            logging.info(' analyzor : i refreshed the price...')
            run_client(f'>>>analyzor : i refreshed the price... => time :: {getTime()["hour"]}:{getTime()["minute"]}')
            length = len( r.json()['Data']['Data'])-1
            # print('len>>>>>>>>>',len( r.json()['Data']['Data'])-1)
            self.price = r.json()['Data']['Data'][length]['close']
            logging.info(' analyzor : i give the datas to rsi func for making the rsi data...')
            run_client(f'>>>analyzor : i give the datas to rsi func for making the rsi data... => time :: {getTime()["hour"]}:{getTime()["minute"]}')
            self.Rsi(r.json())
        except BaseException as error:
            logging.error('someThing went wrong in price func in analyzoe scope...')
            run_client('>>>Oops!I have some issue in analyzing data: {}'.format(error))
    def Rsi(self , data):
        try:
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
            run_client(f'>>>analyzor : making the rsi data succeed... => time :: {getTime()["hour"]}:{getTime()["minute"]}')
                # return (rsi)
        except BaseException as error:
            logging.error('someThing went wrong in price func in analyzoe scope...')
            run_client('>>>Oops!I have some issue in analyzing data: {}'.format(error))

        
    def calculate(self):
        logging.info(' analyzor : start the analyze algorithm succeed...')
        run_client(f'>>>analyzor : start the analyze algorithm succeed... => time :: {getTime()["hour"]}:{getTime()["minute"]}')
        self.Price()
        return ({'price' : self.price , 'rsi' : self.rsi})
        run_client(f'>>>analyzor : data is {{"price" : self.price , "rsi" : self.rsi}} => time :: {getTime()["hour"]}:{getTime()["minute"]}')


