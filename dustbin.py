from pymongo import MongoClient;
from bson.objectid import ObjectId
import datetime

class DustBin:
    def __init__(self):
        self.mongo_url = "mongodb://cmpe297:cmpe297@ds143156.mlab.com:43156/cmpe297"
        self.mongo_db = "cmpe297"
        self.mongo_db_collection = "Trash"
        self.mongo_db_collection_log = "TrashLogs"
        self.bin_id = "5bfeef7033a5340fd7215b7a"
        self.bin_max_height = 198
        self.prev_dustbin_height = 198
        self.bin_location = "MLK Library"
        self.client = MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_db_collection]
        self.trash_log_collection = self.db[self.mongo_db_collection_log]

    def updateBin(self,height):
        print ("updateBin current height : ",height)
        #print (height)
        #print (self.client)
        #print(self.collection)
        now = datetime.datetime.now().isoformat().split(".")[0]
        d={"height":height,"timestamp":now}
        try:
            if(abs(self.prev_dustbin_height - height) > 5):
                print("*****Updating database*******")
                self.collection.update_one({"_id":ObjectId(self.bin_id)},{ "$set": { "capacity": height, "timestamp": now}});
                self.trash_log_collection.insert_one({"max_height":self.bin_max_height,"current_height":height, "timestamp": now,"bin_id":self.bin_id})
                self.collection.insert_one({})
                self.prev_dustbin_height = height
                if(abs(self.bin_max_height - height) < 20):
                    print("Dustbin is almost full !!!")
            else:
                print("Nothing got added !!!")
        except Exception as e:
            print ("error")
            print (e)
