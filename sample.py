from pymongo import MongoClient;
from bson.objectid import ObjectId
# from twilio.rest import Client
import datetime

class Trash:
    def __init__(self):
        self.mongo_url = "mongodb://cmpe297:cmpe297@ds143156.mlab.com:43156/cmpe297"
        # self.mongo_url = "mongodb://arihantsaiparuchuru:Arihant123@ds041157.mlab.com:41157/trash-capacity-notifier"
        self.mongo_db = "cmpe297"
        self.mongo_db_collection = "TrashCapacity"
        self.bin_id = "5bfeef7033a5340fd7215b7attt"
        self.bin_max_height = 300
        self.bin_location = "MLK Library"
        self.client = MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_db_collection]

    '''def sendMessage(self,height):
    	account_sid = 'AC23077766b89b43b4b33b5dd31e396dab'
	    auth_token = '4885dc1d2ac83e2abbc00ba725f88ada'
	    client = Client(account_sid, auth_token)
	    msg = "The bin placed at "+self.bin_location+" is about to get completely filled. It needs assitance."
	    message = client.messages.create(body=msg,from_='+19133183697',to='+16692138942')
	    print("Message SID :",message.sid)'''

    def updateBin(self,height):
        print ("updateBin: ")
        print (height)
        print (self.client)
        print(self.collection)
        now = datetime.datetime.now().isoformat().split(".")[0]
        d={"height":height,"timestamp":now}
        try:
            #self.collection.insert_one({"_id":ObjectId(self.bin_id)},{ "$addToSet": { "capacity": d } });
            self.collection.update_one({"_id":ObjectId(self.bin_id)},{ "$set": { "capacity": d } });
            #self.collection.update_one({"_id":ObjectId(self.bin_id)},{ "$addToSet": { "capacity": d } })
            # if(abs(self.bin_max_height-height)<20):
            # 	self.sendMessage(height)
        except:
            # with open("bin.log","a+") as f:
            #     f.write("Connection Error on : "+now+" | "+str(d)+"\n")
            print ("error")
""""
new_data = [
    {"location":"MLK Floor 1","max_height":"200","capacity":[]},
    {"location":"MLK Floor 2","max_height":"200","capacity":[]}
]
"""
"""
bin = Trash()
for i in range(300,320):
    bin.updateBin(i)
"""
