

import time
import position 
# import requests
import datetime
import analyzor
import logging



logging.basicConfig(format='%(asctime)s:%(levelname)s:>>>>>%(message)s', level=logging.DEBUG , datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug('hello ,  im spider and start the analyze the market for trading')





position = position.Position()

data = analyzor.data()

def getTime():
    return {'hour' : int(datetime.datetime.now().hour) , 'minute' : int(datetime.datetime.now().minute) }


while True:
    time.sleep(25)
    if (getTime()['minute'] == 30):
        logging.info('main=> time for checking the price...')
        cData = data.calculate()
        if (position.state == 0):               # waiting for coming the price to my zone
            logging.info('main=> im waiting for coming the price to my zone...')
            if (cData['rsi'] < 30 or cData['rsi'] > 70):
                logging.info('main=> market is in my zone...')
                position.changeStatus(1 , cData)
                time.sleep(60)

        elif(position.state == 1):            # waiting for making the buttom or top level
            logging.info('main=> i am waiting for making the buttom or top level...')
            if ((cData['rsi'] > 70 and cData['price'] < position.maxTouch.price) or (cData['rsi']<30 and cData['price'] > position.minTouch.price)):
                logging.info('main=> the top zone made in the market ....')
                position.changeStatus(2 , cData)
                time.sleep(60)
            elif ((cData['rsi'] > 70 and cData['price'] > position.maxTouch.price) or (cData['rsi']<30 and cData['price'] < position.minTouch.price)):
                if (cData['rsi'] > 70):
                    logging.info('main=> the max price updated to the upper price ....')
                    position.updatePrice(cData , 1)
                    time.sleep(60)
                elif(cData['rsi']<30):
                    logging.info('main=> the min price updated to the lower price ....')
                    position.updatePrice(cData , 0)
                    time.sleep(60)
        elif(position.state == 2):          # waiting for making retouch the top or buttom
            logging.info('main=> im waiting for making retouch the top or buttom ...')
            if (position.positionType == 0):
                if (cData['price'] in range(position.minTouch.price-(position.minTouch.price*0.005) , position.minTouch.price+(position.minTouch.price*0.005))):
                    logging.info('main=> wow! the market retouch the zone...')
                    position.changeStatus(3 , cData)
                    time.sleep(60)
                elif(cData['price'] < position.minTouch.price-(position.minTouch.price*0.005) ):
                    logging.info('main=> shit the zone was not stable and break...')
                    position.changeStatus(1 , cData)
                    time.sleep(60)
            else:
                if (cData['price'] in range(position.maxTouch.price-(position.maxTouch.price*0.005) , position.maxTouch.price+(position.maxTouch.price*0.005))):
                    logging.info('main=> wow! the market retouch the zone...')
                    position.changeStatus(3 , cData)
                    time.sleep(60)
                elif(cData['price'] > position.maxTouch.price-(position.maxTouch.price*0.005)):
                    logging.info('main=> shit the zone was not stable and break...')
                    position.changeStatus(1 , cData)
                    time.sleep(60)
                
        elif(position.state == 3):         # waiting for approv the divergance
            logging.info('main=> im waiting for approv the divergance')
            if (position.positionType == 0):
                if (cData['price'] > position.minTouch.price):
                    if (position.divergance > position.minTouch.rsi):
                        logging.info('main=> the divergance happended....')
                        position.changeStatus(4 , cData)

                elif(cData['price'] < position.minTouch.price):
                    logging.info('main=> shit the zone was not stable and break...')
                    position.changeStatus(1 , cData)
                    time.sleep(60)
                    

            else:
                if (cData['price'] > position.minTouch.price):
                    if (position.divergance < position.maxTouch.rsi):
                        logging.info('main=> the divergance happended....')
                        position.changeStatus(4 , cData)
                elif(cData['price'] > position.maxTouch.price):
                    logging.info('main=> shit the zone was not stable and break...')
                    position.changeStatus(1 , cData)
                    time.sleep(60)


        elif(position.state == 4):            # waiting for back to the safeZone
            logging.info('main=> im waiting for back to the safeZone')
            if (cData['rsi'] > 30 and cData['rsi'] < 70):
               logging.info('main=> market is in the safe zone...')
               position.refresh()
               time.sleep(60)
     