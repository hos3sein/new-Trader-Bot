
import time
# import requests
import datetime
import logging
import socketio
import pytz
# import subprocess
# IP = subprocess.check_output('wmic bios get serialnumber').decode("utf-8") 
# # IP=[(k, addr.address) for k, v in psutil.net_if_addrs().items() for addr in v if addr.family == -1]
# print(IP)
sio = socketio.SimpleClient()
sio.connect('https://test.spider-cryptobot.site', namespaces='/position' )


def message(msg):
    sio.emit('analyzor', {'data' : msg})



def getTime():
    #return {'hour' : int(datetime.datetime.now().hour) , 'minute' : int(datetime.datetime.now().minute) }
    newYork = pytz.timezone("America/New_York")
    return {'hour' : int(datetime.datetime.now(newYork).hour) , 'minute' : int(datetime.datetime.now(newYork).minute) }



logging.basicConfig(format='%(asctime)s:%(levelname)s:>>>>>%(message)s', level=logging.DEBUG , datefmt='%m/%d/%Y %I:%M:%S %p')
#logging.info(' position : i made the instance for the position...')
#message(' position : i made the instance for the position...')


class Position():
    def __init__(self):
        #logging.info(' position : i made the instance for the position...')
        message(f'>>>position : i made the instance for the position...=> time :: {getTime()["hour"]}:{getTime()["minute"]}')
        self.positionType = None
        self.state = 0
        self.isActive = False
        self.reTouch = None
        self.divergance = None
        self.maxTouch={'price' : None , 'rsi' :None }
        self.minTouch={'price' : None , 'rsi' :None }



    def changeStatus(self , status , cData):
        try:
            logging.info(f'position : the status will change to => {status}')
            message(f'>>>position : the status will change to => {status}=> time :: {getTime()["hour"]}:{getTime()["minute"]}')
            if (status == 1):
                self.state == 1
                self.isActive=True
                logging.info(f'position : the position activate successfully in {cData}')
                message(f'>>>position : the position activate successfully in {cData}=> time :: {getTime()["hour"]}:{getTime()["minute"]}')
                if (cData['rsi']<30):
                    self.minTouch['price'] = cData['price']
                    self.minTouch['rsi'] = cData['rsi']
                    self.positionType = 0
                    logging.info(f'position : the minTouch successfully set and waiting for market to make the buttom in price => {cData}')
                    message(f'>>>position : the minTouch successfully set and waiting for market to make the buttom in price => {cData}=> time :: {getTime()["hour"]}:{getTime()["minute"]}')
                elif(cData['rsi']>70):
                    self.maxTouch['price'] = cData['rsi']
                    self.maxTouch['rsi'] = cData['rsi']
                    self.positionType = 1
                    logging.info(f'position : the maxTouch successfully set and waiting for market to make the top zone in price => {cData}')
                    message(f'>>>position : the maxTouch successfully set and waiting for market to make the top zone in price => {cData}=> time :: {getTime()["hour"]}:{getTime()["minute"]}')
            if (status == 2):
                self.state = 2
                logging.info(f'position : the {"buttom" if self.positionType == 0 else "top zone"} made successfully and waiting for the retouch...')
                message(f'>>>position : the {"buttom" if self.positionType == 0 else "top zone"} made successfully and waiting for the retouch...=> time :: {getTime()["hour"]}:{getTime()["minute"]}')
            if (status == 3):
                self.state = 3
                self.reTouch = cData['rsi']
                self.divergance == cData['rsi']
                logging.info(f'position : the retourch done successfully in price {cData["rsi"]} ')
                message(f'>>>position : the retourch done successfully in price {cData["rsi"]} => time :: {getTime()["hour"]}:{getTime()["minute"]}')
            if (status == 4):
                logging.info(f'position : the divergance successfully approved and i will notif user the position')
                message(f'position : the divergance successfully approved and i will notif user the position=> time :: {getTime()["hour"]}:{getTime()["minute"]}')
                message(f'>>>attention grandPa >>>>>>> its time to {f"BUY the ETH on price {cData["price"]}" if self.positionType == 0 else f"SELL the ETH on price {cData["price"]}"} => time :: {getTime()["hour"]}:{getTime()["minute"]}')
                if (self.positionType == 0):
                    
                    print('its time to buy')
                    message(f'>>> position :: its time to BUY the ETH on price {cData["price"]} => time :: {getTime()["hour"]} : {getTime()["minute"]}')
                elif(self.positionType == 1):
                    print('its time to sell')
                    message(f'>>> position :: its time to SELL the ETH on price {cData["price"]} => time :: {getTimee()["hout"]}:{getTime()["minute"]}')
        except BaseException as error:
            message('>>>Oops!I have some issue in changin status from the position : {}'.format(error))





    def updatePrice(self , data , type):
        try:
            if (type == 1):
                self.maxTouch['price'] = data.price
                self.maxTouch['rsi'] = data.rsi
            if (type == 0):
                self.minTouch['price'] = data.price
                self.minTouch['rsi'] = data.rsi
        except BaseException as error:
            message('Oops!I have some issue in updating Price in function in making position : {}'.format(error))
    
    def refresh(self):
        self.positionType = None
        self.state = 0
        self.isActive = False
        self.reTouch = None
        self.divergance = None
        self.maxTouch={'price' : None , 'rsi' :None }
        self.minTouch={'price' : None , 'rsi' :None }
    
