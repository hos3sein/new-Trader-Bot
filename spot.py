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
c = data.calculate()
lastPrice = c['price']
safeZone = True
message(f'im also watching the market for spot positions ')

while True:

    if (getTime()['minute'] == 59 and int(datetime.datetime.now(pytz.timezone("America/New_York")).second) >= 58):
        print("<><><><><> its time <><><><><><>")
        cData = data.calculate()
        if (cData['rsi'] > 30 and cData['rsi']<70):                     # when the price was on the safe zone
            lastPrice = cData['price']
            safeZone = True                                              # make the safeZone true 
            message(f' spot , the price is on the safe zone in the time {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}')
            # time.sleep(40)

        elif(cData['rsi'] < 30 and safeZone == True):                    # if the price under the 30
            safeZone = False                              # first make the safeZone false 
            if (buyStatus == 0 and sellStatus > 0):                                         # check the buy status if it was 0
                percent = ((cData['price']-lastPrice)/lastPrice)*100
                buyStatus = 1                          
                lastPrice = cData['price']                               # save the last price
                message(f'spot , its time to enter to the level.1 in time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                sellStatus -= 1
                # time.sleep(40)
            ### if the status was 1
            ### we need to check the fucking prices diffrent 
            elif(buyStatus == 1 and sellStatus > 0):                                        # if the status was 1 it means that the price was not come back to safe zone
                if ((abs(cData['price']-lastPrice)/lastPrice)*100 > 8 ): # if the diffrent price percent was more than 5% buy again
                    percent = ((cData['price']-lastPrice)/lastPrice)*100
                    lastPrice = cData['price']
                    buyStatus = 2
                    message(f'spot , its time to enter to the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                    sellStatus -= 1
                    # time.sleep(40)
            elif(buyStatus == 2 and sellStatus > 0):
                if ( (abs(cData['price']-lastPrice)/lastPrice)*100 > 8):
                    percent = (cData['price']-lastPrice)/lastPrice*100
                    buyStatus = 3
                    lastPrice = cData['price']
                    sellStatus -= 1
                    message(f'spot ,ts time to enter to the level.3 in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                    # time.sleep(40)


        elif(cData['rsi'] < 30 and safeZone == False):
            if(buyStatus == 1 and sellStatus > 0):
                if ((abs(cData['price']-lastPrice)/lastPrice) * 100 > 5):
                    percent = (cData['price']-lastPrice)/lastPrice*100
                    buyStatus = 2
                    lastPrice = cData['price']
                    message(f'spot , its time to enter to the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {((cData['price']-lastPrice)/lastPrice)*100}') if cData['price'] < (lastPrice-(0.1*lastPrice)) else message(f'prit ,s not break enough in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                    sellStatus -= 1
                    # time.sleep(40)
            elif(buyStatus == 2 and sellStatus > 0):
                if ( (abs(cData['price']-lastPrice)/lastPrice)*100 > 8):
                    percent = (cData['price']-lastPrice)/lastPrice*100
                    buyStatus = 3
                    lastPrice = cData['price']
                    sellStatus -= 1
                    message(f'spot , its time to enter to the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]}, the change percent is {((cData['price']-lastPrice)/lastPrice)*100}') if cData['price'] < (lastPrice-(0.05*lastPrice)) else message(f'prit ,s not break enough in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                    # time.sleep(40)



        elif(cData['rsi'] > 70 and safeZone == True):
            safeZone = False
            if (sellStatus == 0 and buyStatus > 0):
                percent = (cData['price']-lastPrice)/lastPrice*100
                sellStatus = 1
                lastPrice = cData['price']
                message(f'spot , its time to get out from the level.1 in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                buyStatus -= 1
                # time.sleep(40)
                
            elif(sellStatus == 1 and  buyStatus > 0):
                if (((cData['price']-lastPrice)/lastPrice)*100 > 8):
                    percent = ((cData['price']-lastPrice)/lastPrice)*100
                    sellStatus = 2
                    lastPrice = cData['price']
                    message(f'its time to get out from the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                    buyStatus -= 1 
                    # time.sleep(40)
            elif(sellStatus == 2 and buyStatus > 0):
                if (((cData['price']-lastPrice)/lastPrice)*100 > 8):
                    percent = ((cData['price']-lastPrice)/lastPrice)*100
                    sellStatus = 3
                    lastPrice = cData['price']
                    message(f'spot , its time to get out from the level.3 in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                    buyStatus -= 1
                    # time.sleep(40)


        elif(cData['rsi'] > 70 and safeZone == False):
            if(sellStatus == 1 and buyStatus > 0):
                if (((cData['price']-lastPrice)/lastPrice)*100 > 8):
                    percent = ((cData['price']-lastPrice)/lastPrice)*100
                    sellStatus = 2
                    message(f'spot , its time to get out from the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent') if cData['price'] < (lastPrice+(0.1*lastPrice)) else message(f'prit ,s not top up enough in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                    lastPrice = cData['price']
                    buyStatus -= 1
                    # time.sleep(40)
            elif(sellStatus == 2 and buyStatus > 0):
                if (((cData['price']-lastPrice)/lastPrice)*100 > 8):
                    percent = ((cData['price']-lastPrice)/lastPrice)*100
                    sellStatus = 3
                    message(f'spot , its time to get out from the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ') if cData['price'] < (lastPrice+(0.05*lastPrice)) else message(f'prit ,s not top up enough in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent')
                    lastPrice = cData['price']
                    buyStatus -= 1
                    # time.sleep(40)

    # time.sleep(40)
