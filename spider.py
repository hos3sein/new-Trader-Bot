

import time
import position 
import requests
import datetime
import analyzor


# state = 0
# rsi = 0
# price = 0
# isActive=False
# positionType = None                       # 0 : short   1 : long
# maxTouch = {price : price , rsi : rsi}
# minTouch = {price : price , rsi : rsi}
# reTouch=None
# divergance = None



position = position.Position()
print(position.maxTouch)

data = analyzor.data()

print(data.calculate())


# while True:
    # if (state == 0):               # waiting for coming the price to my zone
    #     if (rsi < 30 or rsi > 70):
    #         # True if fruit == 'Apple' else False
    #         state = 1
    #         isActive=True
    #         if (rsi<30):
    #             minTouch.price = price
    #             minTouch.rsi = rsi
    #             positionType = 0
    #             time.sleep(60*60)
    #         elif(rsi>70):
    #             maxTouch.price = price
    #             maxTouch.rsi = rsi
    #             positionType = 1
    #             time.sleep(60*60)

    # elif(state == 1):            # waiting for making the buttom or top level
    #     if ((rsi > 70 and price < maxTouch.price) or (rsi<30 and price > minTouch.price)):
    #         state = 2
    #         time.sleep(60*60)
    #     elif ((rsi > 70 and price > maxTouch.price) or (rsi<30 and price < minTouch.price)):
    #         if (rsi > 70):
    #             maxTouch.price = price
    #             maxTouch.rsi = rsi
    #             time.sleep(60*60)
    #         elif(rsi<30):
    #             minTouch.price = price
    #             minTouch.rsi = rsi
    #             time.sleep(60*60)
    # elif(state == 2):          # waiting for making retouch the top or buttom
    #     if (positionType == 0):
    #         if (price in range(minTouch.price-(minTouch.price*0.005) , minTouch.price+(minTouch.price*0.005))):
    #             # reTouch = price
    #             state = 3
    #             divergance = rsi
    #             time.sleep(60*60)
    #         elif(price < minTouch.price-(minTouch.price*0.005) ):
    #             minTouch.price = price
    #             minTouch.rsi = rsi
    #             state = 1
    #             time.sleep(60*60)
    #     else:
    #         if (price in range(maxTouch.price-(maxTouch.price*0.005) , maxTouch.price+(maxTouch.price*0.005))):
    #             # reTouch = price
    #             state = 3
    #             divergance = rsi
    #             time.sleep(60*60)
    #         elif(price > maxTouch.price-(maxTouch.price*0.005)):
    #             maxTouch.price = price
    #             maxTouch.rsi = rsi
    #             state = 1
    #             time.sleep(60*60)
            
    # elif(state == 3):         # waiting for approv the divergance
    #     if (positionType == 0):
    #         if (price > minTouch.price):
    #             if (divergance > minTouch.rsi):
    #                 state = 4
    #                 #! notif
    #         elif(price < minTouch.price):
    #             minTouch.price = price
    #             minTouch.rsi = rsi
    #             state = 1
    #             time.sleep(60*60)
                

    #     else:
    #         if (price > minTouch.price):
    #             if (divergance < maxTouch.rsi):
    #                 state = 4
    #                 #! notif
    #         elif(price > maxTouch.price):
    #             maxTouch.price = price
    #             maxTouch.rsi = rsi
    #             state = 1
    #             time.sleep(60*60)


    # elif(state == 4):            # waiting for back to the safeZone
    #     if (rsi > 30 and rsi < 70):
    #         state = 0
    #         isActive=False
    #         positionType = None 
    #         reTouch=None
    #         divergance = None
    #         time.sleep(60*60)