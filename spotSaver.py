import requests 

class requester:
    def __init__(self):
        self.newPositionUrl = 'localhost:7000/spider'
        self.newLogUrl = 'localhost:7000/spider/addNewLog'
        
        
        
        
    def newPosition(self , data):
        req = requests.request("POST", self.newPositionUrl , body=data , headers={})
        print(req.json())
        pass

    
    def newLog(self , data):
        req = requests.request("POST", self.newLogUrl , body=data , headers={})
        print(req)
        pass
    
    