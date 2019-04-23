from pymongo import MongoClient;
from bson.objectid import ObjectId
from twilio.rest import Client
import datetime

class DustBin:
    def __init__(self):
        self.mongo_url = "mongodb://cmpe297:cmpe297@ds143156.mlab.com:43156/cmpe297"
        self.mongo_db = "cmpe297"
        self.mongo_db_collection = "TrashCapacity"
        self.mongo_db_collection_log = "TrashLogs"
        self.bin_id = "5bfeef7033a5340fd7215b7a"
        self.bin_max_height = 198
        self.prev_dustbin_height = 198
        self.bin_location = "MLK Library"
        self.client = MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_db_collection]
        self.trash_log_collection = self.db[self.mongo_db_collection_log]

    def sendSMS(self):
        account_sid = 'AC67863e4c5ec2c424ecf5cc26ec466d36'
        auth_token = '7a7f1773699682ed4de7b8b1b976ac59'
        client = Client(account_sid, auth_token)
        msg = "The bin placed at " + " MLK LIbrary" + " is about to get completely filled. It needs assitance."
        message = client.messages.create(body = msg,from_ = '+15128569912',to = '+15122010228')
        print("Message SID :",message.sid)


    def updateBin(self,height):
        print ("updateBin current height : ", height)
        if not(height >= 1 and height <= self.bin_max_height):
            print("Height out of range !!!")
            return
        now = datetime.datetime.now()
        d = {"height":height,"timestamp":now}
        try:
            if(abs(self.prev_dustbin_height - height) > 5):
                print("*****Updating database*******\n\n")
                self.collection.update_one({"_id":ObjectId(self.bin_id)},{ "$set": { "capacity": (self.bin_max_height - height), "timestamp": now}});
                self.trash_log_collection.insert_one({"max_height":self.bin_max_height,"current_height":(self.bin_max_height - height), "timestamp": now,"bin_id":self.bin_id})
                self.prev_dustbin_height = height
                if(abs(self.bin_max_height - height) > 170):
                    print("Dustbin is almost full !!!")
                    self.sendSMS()
            else:
                print("Nothing got added !!!")
            print("\n_______________________________________________________________\n")
        except Exception as e:
            print ("error")
            print (e)
