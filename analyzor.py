
import requests
import datetime
import talib
import pandas as pa
import numpy as np


r = requests.get('https://min-api.cryptocompare.com/data/v2/histohour?fsym=ETH&tsym=USD&limit=50')
# r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD')
print('len>>>>>>>>>',(len( r.json()['Data']['Data'])))
# print(datetime.datetime.fromtimestamp(r.json()['Data']['Data'][1]['time']).strftime('%Y-%m-%d %H:%M:%S'))
# print(datetime.datetime.fromtimestamp(r.json()['Data']['Data'][2]['time']).strftime('%Y-%m-%d %H:%M:%S'))
# print(datetime.datetime.fromtimestamp(r.json()['Data']['Data'][3]['time']).strftime('%Y-%m-%d %H:%M:%S'))
# print(datetime.datetime.fromtimestamp(r.json()['Data']['Data'][9]['time']).strftime('%Y-%m-%d %H:%M:%S'))



openPrice = []
closePrice = []

for i in r.json()['Data']['Data']:
    # print(i)
    openPrice.append(int(i['open']))
    closePrice.append(int(i['close']))

# print(openPrice)

requiredRsi = pa.DataFrame({'open' : openPrice , 'close' : closePrice})

print(requiredRsi['close'])

rsi = talib.RSI(requiredRsi['close'])

print('rsi>>>>>>>>>>>',rsi)

