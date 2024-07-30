
import logging



logging.basicConfig(format='%(asctime)s:%(levelname)s:>>>>>%(message)s', level=logging.DEBUG , datefmt='%m/%d/%Y %I:%M:%S %p')
class Position():
    def __init__(self):
        logging.info(' position : i made the instance for the position...')
        self.positionType = None
        self.state = 0
        self.isActive = False
        self.reTouch = None
        self.divergance = None
        self.maxTouch={'price' : None , 'rsi' :None }
        self.minTouch={'price' : None , 'rsi' :None }



    def changeStatus(self , status , cData):
        logging.info(f'position : the status will change to => ${status}')
        if (status == 1):
            self.state == 1
            self.isActive=True
            logging.info(f'position : the position activate successfully in price')
            if (cData['rsi']<30):
                self.minTouch.price = cData['price']
                self.minTouch.rsi = cData['rsi']
                self.positionType = 0
                logging.info(f'position : the minTouch successfully set and waiting for market to make the buttom in price => ${cData}')
            elif(cData['rsi']>70):
                self.maxTouch.price = cData['rsi']
                self.maxTouch.rsi = cData['rsi']
                self.positionType = 1
                logging.info(f'position : the maxTouch successfully set and waiting for market to make the top zone in price => ${cData}')
        if (status == 2):
            self.state = 2
            logging.info(f'position : the ${'buttom' if self.positionType == 0 else 'top zone'} made successfully and waiting for the retouch...')
        if (status == 3):
            self.state = 3
            self.reTouch = cData['rsi']
            self.divergance == cData['rsi']
            logging.info(f'position : the retourch done successfully in price ${cData['rsi']} ')
        if (status == 4):
            logging.info(f'position : the divergance successfully approved and i will notif user the position')
            if (self.positionType == 0):
                
                print('its time to buy')

            elif(self.positionType == 1):
                print('its time to sell')





    def updatePrice(self , data , type):
        if (type == 1):
            self.maxTouch.price = data.price
            self.maxTouch.rsi = data.rsi
        if (type == 0):
            self.minTouch.price = data.price
            self.minTouch.rsi = data.rsi


    def refresh(self):
        self.positionType = None
        self.state = 0
        self.isActive = False
        self.reTouch = None
        self.divergance = None
        self.maxTouch={'price' : None , 'rsi' :None }
        self.minTouch={'price' : None , 'rsi' :None }
    