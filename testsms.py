from twilio.rest import Client
def sendSMS():
        account_sid = 'ACe203774c5b6444314a8cb85872d5fa40'
        auth_token = 'c8a6dc2aa268c86b009a5923f0dae718'
        client = Client(account_sid, auth_token)
        msg = "The bin placed at " + " MLK LIbrary" + " is about to get completely filled. It needs assitance."
        message = client.messages.create(body = msg,from_ = '+12024101410',to = '+16692526739')
        print("Message SID :",message.sid)
        
print("Testing .......")
sendSMS()
