
import time
import position 
# import requests
import datetime
import analyzor
import logging
import socketio
import pytz
import psutil
IP=[(k, addr.address) for k, v in psutil.net_if_addrs().items() for addr in v if addr.family == -1]

sio = socketio.SimpleClient()
sio.connect('https://test.spider-cryptobot.site', namespaces='/futures' ,  headers = {'MACAddress' : IP[len(IP)-1]})

def run_client(msg):
    sio.emit('new message', {'data' : msg})




print(socketio.__file__)

logging.basicConfig(format='%(asctime)s:%(levelname)s:>>>>>%(message)s', level=logging.DEBUG , datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug('hello ,  im spider and start the analyze the market for trading')
#run_client('hello ,  im spider and start the analyze the market for trading')


position = position.Position()

data = analyzor.data()


def getTime():
    newYorkTz = pytz.timezone("America/New_York")
    #timeInNewYork = datetime.now(newYorkTz)
    return {'hour' : int(datetime.datetime.now(newYorkTz).hour) , 'minute' : int(datetime.datetime.now(newYorkTz).minute) }

logging.info(' position : i made the instance for the position...')
run_client('>>>position : i made the instance for the position...')



while True:
    #run_client(f'main = > its for test babay {getTime()["hour"]} : {getTime()["minute"]}' )
    time.sleep(40)
    if (getTime()['minute'] == 59):
        logging.info('main  =>  time for checking the price...')
        run_client(f'>>>main  =>  time for checking the price... => time :: {getTime()["hour"]} : {getTime()["minute"]}')
        cData = data.calculate()
        if (position.state == 0):               # waiting for coming the price to my zone
            logging.info('main=> im waiting for coming the price to my zone...')
            run_client(f'>>>main=> im waiting for coming the price to my zone... time :: {getTime()["hour"]} : {getTime()["minute"]}')
            if (cData['rsi'] < 30 or cData['rsi'] > 70):
                logging.info('main=> market is in my zone...')
                run_client(f'>>>main => market is in my zone... => time :: {getTime()["hour"]} : {getTime()["minute"]}')
                position.changeStatus(1 , cData)
                time.sleep(60)

        elif(position.state == 1):            # waiting for making the buttom or top level
            logging.info('main=> i am waiting for making the buttom or top level...')
            run_client(f'>>>main=> i am waiting for making the buttom or top level... => time :: {getTime()["hour"]} : {getTime()["minute"]}')
            if ((cData['rsi'] > 70 and cData['price'] < position.maxTouch.price) or (cData['rsi']<30 and cData['price'] > position.minTouch.price)):
                logging.info('main=> the top zone made in the market ....')
                run_client(f'>>>main=> the top zone made in the market .... => time :: {getTime()["hour"]} : {getTime()["minute"]}')
                position.changeStatus(2 , cData)
                time.sleep(60)
            elif ((cData['rsi'] > 70 and cData['price'] > position.maxTouch.price) or (cData['rsi']<30 and cData['price'] < position.minTouch.price)):
                if (cData['rsi'] > 70):
                    logging.info('main=> the max price updated to the upper price ....')
                    run_client(f'>>>main=> the max price updated to the upper price .... => time :: {getTime()["hour"]} : {getTime()["minute"]}')
                    position.updatePrice(cData , 1)
                    time.sleep(60)
                elif(cData['rsi']<30):
                    logging.info('main=> the min price updated to the lower price ....')
                    run_client(f'>>>main=> the min price updated to the lower price .... => time :: {getTime()["hour"]} : {getTime()["minute"]}')
                    position.updatePrice(cData , 0)
                    time.sleep(60)
        elif(position.state == 2):          # waiting for making retouch the top or buttom
            logging.info('main=> im waiting for making retouch the top or buttom ...')
            run_client(f'>>>main=> im waiting for making retouch the top or buttom ... => time :: {getTime()["hour"]} : {getTime()["minute"]}')
            if (position.positionType == 0):
                if (cData['price'] in range(position.minTouch.price-(position.minTouch.price*0.005) , position.minTouch.price+(position.minTouch.price*0.005))):
                    logging.info('main=> wow! the market retouch the zone...')
                    run_client(f'>>>main=> wow! the market retouch the zone... => time :: {getTime()["hour"]} : {getTime()["minute"]}')
                    position.changeStatus(3 , cData)
                    time.sleep(60)
                elif(cData['price'] < position.minTouch.price-(position.minTouch.price*0.005) ):
                    logging.info('main=> shit the zone was not stable and break...')
                    run_client(f'>>>main=> shit the zone was not stable and break... => time :: {getTime()["hour"]} : {getTime()["minute"]}')
                    position.changeStatus(1 , cData)
                    time.sleep(60)
            else:
                if (cData['price'] in range(position.maxTouch.price-(position.maxTouch.price*0.005) , position.maxTouch.price+(position.maxTouch.price*0.005))):
                    logging.info('main=> wow! the market retouch the zone...')
                    run_client(f'>>>main=> wow! the market retouch the zone...=> time :: {getTime()["hour"]} : {getTime()["minute"]}')
                    position.changeStatus(3 , cData)
                    time.sleep(60)
                elif(cData['price'] > position.maxTouch.price-(position.maxTouch.price*0.005)):
                    logging.info('main=> shit the zone was not stable and break...')
                    run_client(f'>>>main=> shit the zone was not stable and break...=> time :: {getTime()["hour"]} : {getTime()["minute"]}')
                    position.changeStatus(1 , cData)
                    time.sleep(60)
                
        elif(position.state == 3):         # waiting for approv the divergance
            logging.info('main=> im waiting for approv the divergance')
            run_client(f'>>>main=> im waiting for approv the divergance => time :: {getTime()["hour"]} : {getTime()["minute"]}')
            if (position.positionType == 0):
                if (cData['price'] > position.minTouch.price):
                    if (position.divergance > position.minTouch.rsi):
                        logging.info('main=> the divergance happended....')
                        run_client(f'>>>main=> the divergance happended.... => time :: {getTime()["hour"]} : {getTime()["minute"]}')
                        position.changeStatus(4 , cData)
                    time.sleep(60)
                elif(cData['price'] < position.minTouch.price):
                    logging.info('main=> shit the zone was not stable and break...')
                    run_client(f'>>>main=> shit the zone was not stable and break...=> time :: {getTime()["hour"]} : {getTime()["minute"]}')
                    position.changeStatus(1 , cData)
                    time.sleep(60)
                    

            else:
                if (cData['price'] > position.minTouch.price):
                    if (position.divergance < position.maxTouch.rsi):
                        logging.info('main=> the divergance happended....')
                        run_client(f'>>>main=> the divergance happended.... => time :: {getTime()["hour"]} : {getTime()["minute"]}')
                        position.changeStatus(4 , cData)
                    time.sleep(60)
                elif(cData['price'] > position.maxTouch.price):
                    logging.info('main=> shit the zone was not stable and break...')
                    run_client(f'>>>main=> shit the zone was not stable and break...=> time :: {getTime()["hour"]} : {getTime()["minute"]}')
                    position.changeStatus(1 , cData)
                    time.sleep(60)


        elif(position.state == 4):            # waiting for back to the safeZone
            logging.info('main=> im waiting for back to the safeZone')
            run_client(f'>>>main=> im waiting for back to the safeZone => time :: {getTime()["hour"]} : {getTime()["minute"]}')
            if (cData['rsi'] > 30 and cData['rsi'] < 70):
               logging.info('main=> market is in the safe zone...')
               run_client(f'>>>main=> im waiting for back to the safeZone => {getTime()["hour"]} : {getTime()["minute"]}')
               position.refresh()
               time.sleep(60)
         
