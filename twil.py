import os
from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACf34a7eb9833912a41f4dc2f2c76dd6b1"
# Your Auth Token from twilio.com/console
auth_token  = "ed9379bbdb4969a49cb5f59b46906176"

client = Client(account_sid, auth_token)

message = client.conversations \
    .conversations('CHb4aaccd27a5047268f6c63543718033c') \
    .messages \
    .create(
         body='Hey! This is the study group for BM 2022 and we will be meeting on Tuesday 1:30 PM-2:20 PM in Walc3078!',
         author='twilio'
     )

print(message.sid)

#message = client.messages.create(
 #   to="+19148067766", 
  #  from_="+16073005429",
   # body="Am I an Iphone?")

#print(message.sid)