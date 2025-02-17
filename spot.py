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
lastStatus = 'buy'              # for the time that i want to check the percent filter
message(f'the spot bot restart in time {getTime()["hour"]}:{getTime()["minute"]} ')

while True:
    if (getTime()['minute'] == 59 and int(datetime.datetime.now(pytz.timezone("America/New_York")).second) >= 58 and int(datetime.datetime.now(pytz.timezone("America/New_York")).second) <= 59):
        print("<><><><><> its time <><><><><><>")
        cData = data.calculate()
        if (cData['rsi'] > 30 and cData['rsi'] < 70):                     # when the price was on the safe zone
            percent = ((cData['price']-lastPrice)/lastPrice)*100
            safeZone = True                                              # make the safeZone true 
            message(f' spot , the price is on the safe zone in the time {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the last price is {lastPrice} , the percent changes is {percent}')

           

        elif(cData['rsi'] < 30 and safeZone == True):                 # if the price under the 30
            safeZone = False                              # first make the safeZone false
            if (buyStatus == 0):
                percent = ((cData['price']-lastPrice)/lastPrice)*100
                buyStatus += 1                          
                lastPrice = cData['price']                               # save the last price
                sellStatus -= 1
                lastStatus = 'buy'
                message(f'spot , its time to enter to the level.{buyStatus+1}  in time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
            if (buyStatus > 0):
                if (lastStatus == 'sell'):
                    percent = ((cData['price']-lastPrice)/lastPrice)*100
                    lastPrice = cData['price']
                    buyStatus += 1
                    safeZone = False                              # first make the safeZone false 
                    sellStatus -= 1
                    lastStatus = 'buy'
                    message(f'spot , its time to enter to the level.{buyStatus+1} in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                else:
                    if ((abs(cData['price']-lastPrice)/lastPrice)*100 > 8): # if the diffrent price percent was more than 5% buy again
                        percent = ((cData['price']-lastPrice)/lastPrice)*100
                        lastPrice = cData['price']
                        buyStatus += 1
                        safeZone = False                              # first make the safeZone false 
                        sellStatus -= 1
                        lastStatus = 'buy'
                        message(f'spot , its time to enter to the level.{buyStatus+1}  in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                    else:
                        percent = ((cData['price']-lastPrice)/lastPrice)*100
                        message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')    
                        
                        
                    
            # if (buyStatus == 0 and sellStatus > 0):                                         # check the buy status if it was 0
            #     percent = ((cData['price']-lastPrice)/lastPrice)*100
            #     buyStatus = 1                          
            #     lastPrice = cData['price']                               # save the last price
            #     sellStatus -= 1
            #     message(f'spot , its time to enter to the level.1 in time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                
         
            # ### if the status was 1
            # ### we need to check the fucking prices diffrent 
            # elif(buyStatus == 1 and sellStatus > 0):                                        # if the status was 1 it means that the price was not come back to safe zone
            #     if ((abs(cData['price']-lastPrice)/lastPrice)*100 > 8 ): # if the diffrent price percent was more than 5% buy again
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         lastPrice = cData['price']
            #         buyStatus = 2
            #         safeZone = False                              # first make the safeZone false 
            #         sellStatus -= 1
            #         message(f'spot , its time to enter to the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
            #     else:
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')    
            #         
            # elif(buyStatus == 2 and sellStatus > 0):
            #     if ((abs(cData['price']-lastPrice)/lastPrice)*100 > 8):
            #         percent = (cData['price']-lastPrice)/lastPrice*100
            #         buyStatus = 3
            #         lastPrice = cData['price']
            #         sellStatus -= 1
            #         safeZone = False                              # first make the safeZone false
            #         message(f'spot ,ts time to enter to the level.3 in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
            #     else:
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')


        elif(cData['rsi'] < 30 and safeZone == False):
            if (buyStatus > 0):
                if (lastStatus == 'sell'):
                    percent = (cData['price']-lastPrice)/lastPrice*100
                    buyStatus += 1 
                    lastPrice = cData['price']
                    sellStatus -= 1
                    lastStatus = 'buy'
                    message(f'spot , its time to enter to the level.{buyStatus+1} in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent}')
                else:
                    if ((abs(cData['price']-lastPrice)/lastPrice) * 100 > 8):
                        percent = (cData['price']-lastPrice)/lastPrice*100
                        buyStatus += 1 
                        lastPrice = cData['price']
                        sellStatus -= 1
                        lastStatus = 'buy'
                        message(f'spot , its time to enter to the level.{buyStatus+1} in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent}')
                    else:
                        percent = ((cData['price']-lastPrice)/lastPrice)*100
                        message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')    
                    
            # if( buyStatus == 1 and sellStatus > 0):
            #     if ((abs(cData['price']-lastPrice)/lastPrice) * 100 > 8):
            #         percent = (cData['price']-lastPrice)/lastPrice*100
            #         buyStatus = 2
            #         lastPrice = cData['price']
            #         sellStatus -= 1
            #         message(f'spot , its time to enter to the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent}')
            #     else:
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')    
            #         
            # elif(buyStatus == 2 and sellStatus > 0):
            #     if ((abs(cData['price']-lastPrice)/lastPrice)*100 > 8):
            #         percent = (cData['price']-lastPrice)/lastPrice*100
            #         buyStatus = 3
            #         lastPrice = cData['price']
            #         sellStatus -= 1
            #         message(f'spot , its time to enter to the level.3 in the time , {getTime()["hour"]}:{getTime()["minute"]},... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent}') 
            #         
            #     else:
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')

        elif(cData['rsi'] > 70 and safeZone == True):
            safeZone = False
            if (buyStatus > 0):
                if (lastStatus == 'buy'):
                    percent = ((cData['price']-lastPrice)/lastPrice)*100
                    sellStatus += 1
                    lastPrice = cData['price']
                    buyStatus -= 1 
                    lastStatus = 'sell'
                    message(f'its time to get out from the level.{buyStatus} in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                    
                else:
                    if (((cData['price']-lastPrice)/lastPrice)*100 > 8):
                        percent = ((cData['price']-lastPrice)/lastPrice)*100
                        sellStatus += 1
                        lastPrice = cData['price']
                        buyStatus -= 1 
                        lastStatus = 'sell'
                        message(f'its time to get out from the level.{buyStatus} in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                        
                    else:
                        percent = ((cData['price']-lastPrice)/lastPrice)*100
                        message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')
            else :
                percent = ((cData['price']-lastPrice)/lastPrice)*100
                message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')
                
            # if (sellStatus == 0 and buyStatus > 0):
            #     percent = (cData['price']-lastPrice)/lastPrice*100
            #     sellStatus = 1
            #     lastPrice = cData['price']
            #     buyStatus -= 1
            #     message(f'spot , its time to get out from the level.1 in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                
            # elif(sellStatus == 1 and  buyStatus > 0):
            #     if (((cData['price']-lastPrice)/lastPrice)*100 > 8):
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         sellStatus = 2
            #         lastPrice = cData['price']
            #         buyStatus -= 1 
            #         message(f'its time to get out from the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
            #         
            #     else:
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')
            # elif(sellStatus == 2 and buyStatus > 0):
            #     if (((cData['price']-lastPrice)/lastPrice)*100 > 8):
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         sellStatus = 3
            #         lastPrice = cData['price']
            #         buyStatus -= 1
            #         message(f'spot , its time to get out from the level.3 in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
            #     else:
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')  
            #         


        elif(cData['rsi'] > 70 and safeZone == False):
            if (buyStatus > 0):
                if (lastStatus == 'buy'):
                    percent = ((cData['price']-lastPrice)/lastPrice)*100
                    sellStatus += 1
                    lastPrice = cData['price']
                    buyStatus -= 1 
                    lastStatus = 'sell'
                    message(f'its time to get out from the level.{buyStatus} in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                    
                else: 
                    if (((cData['price']-lastPrice)/lastPrice)*100 > 8):
                        percent = ((cData['price']-lastPrice)/lastPrice)*100
                        sellStatus += 1
                        lastPrice = cData['price']
                        buyStatus -= 1 
                        lastStatus = 'sell'
                        message(f'its time to get out from the level.{buyStatus} in the time , {getTime()["hour"]}:{getTime()["minute"]} ... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent')
                        
                    else:
                        percent = ((cData['price']-lastPrice)/lastPrice)*100
                        message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')
            else :
                percent = ((cData['price']-lastPrice)/lastPrice)*100
                message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')
 
            # if(sellStatus == 1 and buyStatus > 0):
            #     if (((cData['price']-lastPrice)/lastPrice)*100 > 8):
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         sellStatus = 2
            #         buyStatus -= 1
            #         lastPrice = cData['price']
            #         message(f'spot , its time to get out from the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus}, the change percent is {percent} percent') 
            #     else:
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')       
                    
            #         
            # elif(sellStatus == 2 and buyStatus > 0):
            #     if (((cData['price']-lastPrice)/lastPrice)*100 > 8):
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         sellStatus = 3
            #         lastPrice = cData['price']
            #         buyStatus -= 1
            #         message(f'spot , its time to get out from the level.2 in the time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')
                    
            #         
            #     else:
            #         percent = ((cData['price']-lastPrice)/lastPrice)*100
            #         message(f'spot , the status of the market and spot spider is , time , {getTime()["hour"]}:{getTime()["minute"]}... price is {cData['price']} , rsi is {cData['rsi']} , the safe zone is {safeZone} , the buy status is {buyStatus} , the sell status is {sellStatus} , the change percent is {percent} percent ')
