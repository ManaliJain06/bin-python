from pymongo import MongoClient;
from bson.objectid import ObjectId
from twilio.rest import Client
from datetime import datetime, timedelta

class DustBin:
    def __init__(self):
        self.mongo_url = "mongodb://cmpe297:cmpe297@ds143156.mlab.com:43156/cmpe297"
        self.mongo_db = "cmpe297"
        self.mongo_db_collection = "TrashCapacity"
        self.mongo_db_collection_log = "TrashLogs"
        self.bin_id = "5bfeef7033a5340fd7215b7a"
        self.bin_max_height = 27
        self.prev_dustbin_height = self.bin_max_height
        self.bin_location = "MLK Library"
        self.client = MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_db_collection]
        self.trash_log_collection = self.db[self.mongo_db_collection_log]
        self.shld_update_initial_height = True

    def sendSMS(self):
        account_sid = 'ACe203774c5b6444314a8cb85872d5fa40'
        auth_token = 'c8a6dc2aa268c86b009a5923f0dae718'
        client = Client(account_sid, auth_token)
        msg = "The bin placed at " + " engineering bld. " + " is about to get completely filled. It needs assitance."
        message = client.messages.create(body = msg,from_ = '+12024101410',to = '+16692526739')
        print("Message SID :",message.sid)


    def updateBin(self,height):

        if not(height >= 1 and height <= self.bin_max_height):
            print("Height out of range !!!", height)
            return
        print ("updateBin current height : ", height)
        #now = datetime.datetime.now()
        now = datetime.now() - timedelta(1)
        d = {"height":height,"timestamp":now}
        try:
            if(self.shld_update_initial_height):
                self.collection.insert_one({"_id":ObjectId(self.bin_id), "capacity":0})
                self.shld_update_initial_height = False
            if(abs(self.prev_dustbin_height - height) > 2):
                print("*****Updating database*******\n\n")
                self.collection.update_one({"_id":ObjectId(self.bin_id)},{ "$set": { "capacity": (self.bin_max_height - height), "timestamp": now}});
                self.trash_log_collection.insert_one({"max_height":self.bin_max_height,"current_height":(self.bin_max_height - height), "timestamp": now,"bin_id":self.bin_id})
                self.prev_dustbin_height = height
                if( height <= 5):
                    print("Dustbin is almost full, sending sms alert !!!")
                    self.sendSMS()
            else:
                print("No significant change !!!")
            print("\n_______________________________________________________________\n")
        except Exception as e:
            print ("error")
            print (e)
