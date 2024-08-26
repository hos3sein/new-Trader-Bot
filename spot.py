import analyzor
import socketio
import datetime
import time
import pytz
# import subprocess
# IP = subprocess.check_output('wmic bios get serialnumber').decode("utf-8") 
# # IP=[(k, addr.address) for k, v in psutil.net_if_addrs().items() for addr in v if addr.family == -1]
# print(IP)
sio = socketio.Client()
sio.connect('https://test.spider-cryptobot.site', namespaces='/spot')


def message(msg):
    sio.emit('spot', {'data' : msg} , namespace='/spot')


def getTime():

    newYork = pytz.timezone("America/New_York")
    return {'hour' : int(datetime.datetime.now(newYork).hour) , 'minute' : int(datetime.datetime.now(newYork).minute) }

# print(analyzor.data())

data = analyzor.data()

buyStatus = 0
sellStatus = 3
lastPrice = 0
safeZone = True
message(f'im also watching the market for spot positions ')

while True:
    #message(f'spot ,m also watching the market for spot positions ... ')
    if (getTime()['minute'] == 59):
        cData = data.calculate()
        if (cData['rsi'] > 30 and cData['rsi']<70):                     # when the price was on the safe zone 
            safeZone = True                                              # make the safeZone true 
            message(f' spot , the price is on the safe zone in the time {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}')
            time.sleep(40)

        elif(cData['rsi'] < 30 and safeZone == True):                    # if the price under the 30
            safeZone = False                                             # first make the safeZone false 
            if (buyStatus == 0 and sellStatus > 0):                                         # check the buy status if it was 0
                buyStatus = 1                          
                lastPrice = cData['price']                               # save the last price
                message(f'spot , its time to enter to the level.1 in time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}')
                sellStatus -= 1
                time.sleep(40)
            ### if the status was 1
            ### we need to check the fucking prices diffrent 
            elif(buyStatus == 1 and sellStatus > 0):                                        # if the status was 1 it means that the price was not come back to safe zone
                if ( cData['rsi'] <= 25 ): # if the diffrent price percent was more than 5% buy again
                    lastPrice = cData['price']
                    buyStatus = 2
                    message(f'spot , its time to enter to the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}')
                    sellStatus -= 1
                    time.sleep(40)
            elif(buyStatus == 2 and sellStatus > 0):
                if (cData['rsi'] <= 20):
                    buyStatus = 3
                    lastPrice = cData['price']
                    sellStatus -= 1
                    message(f'spot ,ts time to enter to the level.3 in the time , {getTime()["hour"]}:{getTime()["minute"]}')
                    time.sleep(40)


        elif(cData['rsi'] < 30 and safeZone == False):
            if(buyStatus == 1 and sellStatus > 0):
                if (cData['rsi'] <= 25):
                    buyStatus = 2
                    lastPrice = cData['price']
                    message(f'spot , its time to enter to the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}') if cData['price'] < (lastPrice-(0.1*lastPrice)) else message(f'prit ,s not break enough in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}')
                    sellStatus -= 1
                    time.sleep(40)
            elif(buyStatus == 2 and sellStatus > 0):
                if (cData['rsi'] <= 20):
                    buyStatus = 3
                    lastPrice = cData['price']
                    sellStatus -= 1
                    message(f'spot , its time to enter to the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]}') if cData['price'] < (lastPrice-(0.05*lastPrice)) else message(f'prit ,s not break enough in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}')
                    time.sleep(40)



        elif(cData['rsi'] > 70 and safeZone == True):
            safeZone = False
            if (sellStatus == 0 and buyStatus > 0):
                sellStatus = 1
                lastPrice = cData['price']
                message(f'spot , its time to get out from the level.1 in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}')
                buyStatus -= 1
                time.sleep(40)
                
            elif(sellStatus == 1 and  buyStatus > 0):
                if (cData['rsi'] >= 75):
                    sellStatus = 2
                    lastPrice = cData['price']
                    message(f'its time to get out from the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}')
                    buyStatus -= 1 
                    time.sleep(40)
            elif(sellStatus == 2 and buyStatus > 0):
                if (cData['rsi'] <= 80):
                    sellStatus = 3
                    lastPrice = cData['price']
                    message(f'spot , its time to get out from the level.3 in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}')
                    buyStatus -= 1
                    time.sleep(40)


        elif(cData['rsi'] > 70 and safeZone == False):
            if(sellStatus == 1 and buyStatus > 0):
                if (cData['rsi'] >= 75):
                    sellStatus = 2
                    message(f'spot , its time to get out from the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}') if cData['price'] < (lastPrice+(0.1*lastPrice)) else message(f'prit ,s not top up enough in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}')
                    lastPrice = cData['price']
                    buyStatus -= 1
                    time.sleep(40)
            elif(sellStatus == 2 and buyStatus > 0):
                if (cData['rsi'] >= 80):
                    sellStatus = 3
                    message(f'spot , its time to get out from the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}') if cData['price'] < (lastPrice+(0.05*lastPrice)) else message(f'prit ,s not top up enough in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}')
                    lastPrice = cData['price']
                    buyStatus -= 1
                    time.sleep(40)
    else:
        time.sleep(40)
