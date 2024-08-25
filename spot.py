import analyzor
import socketio
import datetime
import time
import pytz
sio = socketio.SimpleClient()
sio.connect('https://test.spider-cryptobot.site')


def message(msg):
    sio.emit('analyzor', {'data' : msg})


def getTime():

    newYork = pytz.timezone("America/New_York")
    return {'hour' : int(datetime.datetime.now(newYork).hour) , 'minute' : int(datetime.datetime.now(newYork).minute) }

# print(analyzor.data())

data = analyzor.data()

buyStatus = 0
sellStatus = 0
lastPrice = 0
safeZone = True
message(f'im also watching the market for spot positions ... ')

while True:
    time.sleep(40)
    #message(f'>>>spot=>im also watching the market for spot positions ... ')
    if (getTime()['minute'] == 59):
        cData = data.calculate()
        if (cData['rsi'] > 30 and cData['rsi']<70):
            safeZone = True
            message(f'>>> spot=>the price is on the safe zone => time {getTime()["hour"]}:{getTime()["minute"]}')


        elif(cData['rsi'] < 30 and safeZone == True):
            safeZone = False
            if (buyStatus == 0):
                buyStatus = 1
                lastPrice = cData['price']
                message(f'>>>spot => its time to enter to the level.1 => time ::: {getTime()["hour"]}:{getTime()["minute"]}')
            elif(buyStatus == 1):
                buyStatus = 2
                lastPrice = cData['price']
                message(f'>>>spot => its time to enter to the level.2 => time ::: {getTime()["hour"]}:{getTime()["minute"]}')
            elif(buyStatus == 2):
                buyStatus = 3
                lastPrice = cData['price']
                message(f'>>>spot=>its time to enter to the level.3 => time ::: {getTime()["hour"]}:{getTime()["minute"]}')


        elif(cData['rsi'] < 30 and safeZone == False):
            if(buyStatus == 1):
                buyStatus = 2
                message(f'>>>spot => its time to enter to the level.2 => time ::: {getTime()["hour"]}:{getTime()["minute"]}') if cData['price'] < (lastPrice-(0.1*lastPrice)) else message(f'>>>price is not break enough => time ::: {getTime()["hour"]}:{getTime()["minute"]}')
                lastPrice = cData['price']
            elif(buyStatus == 2):
                buyStatus = 3
                message(f'>>>spot => its time to enter to the level.2 => time ::: {getTime()["hour"]}:{getTime()["minute"]}') if cData['price'] < (lastPrice-(0.05*lastPrice)) else message(f'>>>price is not break enough => time ::: {getTime()["hour"]}:{getTime()["minute"]}')
                lastPrice = cData['price']



        elif(cData['rsi'] > 70 and safeZone == True):
            safeZone = False
            if (sellStatus == 0):
                sellStatus = 1
                lastPrice = cData['price']
                message(f'>>>spot => its time to get out from the level.1 => time ::: {getTime()["hour"]}:{getTime()["minute"]}')
            elif(sellStatus == 1):
                sellStatus = 2
                lastPrice = cData['price']
                message(f'>>>its time to get out from the level.2 => time ::: {getTime()["hour"]}:{getTime()["minute"]}')
            elif(sellStatus == 2):
                sellStatus = 3
                lastPrice = cData['price']
                message(f'>>>spot => its time to get out from the level.3 => time ::: {getTime()["hour"]}:{getTime()["minute"]}')


        elif(cData['rsi'] > 70 and safeZone == False):
            if(sellStatus == 1):
                sellStatus = 2
                message(f'>>>spot => its time to get out from the level.2 => time ::: {getTime()["hour"]}:{getTime()["minute"]}') if cData['price'] < (lastPrice+(0.1*lastPrice)) else message(f'>>>price is not top up enough => time ::: {getTime()["hour"]}:{getTime()["minute"]}')
                lastPrice = cData['price']
            elif(sellStatus == 2):
                sellStatus = 3
                message(f'>>>spot => its time to get out from the level.2 => time ::: {getTime()["hour"]}:{getTime()["minute"]}') if cData['price'] < (lastPrice+(0.05*lastPrice)) else message(f'>>>price is not top up enough => time ::: {getTime()["hour"]}:{getTime()["minute"]}')
                lastPrice = cData['price']


