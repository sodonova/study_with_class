import os
from pydoc import cli
from twilio.rest import Client

phonenum = ["3172497574","9148067766", "7658389656", "6147023950"] # "6147023950"


# Your Account SID from twilio.com/console
account_sid = "ACf34a7eb9833912a41f4dc2f2c76dd6b1"
# Your Auth Token from twilio.com/console
auth_token  = "1c35356d92d60326c491a2d896aa30c5"

client = Client(account_sid, auth_token)


# conversation = client.conversations \
#                      .conversations \
#                      .create(friendly_name='Study group')
# message = client.conversations \
#     .conversations(conversation.sid) \
#     .participants \
#                     .create(
#                          identity='twilio',
#                          messaging_binding_projected_address='+16073005429'
#                      )

#for x in phonenum:
 #   client.conversations \
  #                  .conversations('CHaca7ccf263504d7589898b02eee805b5') \
   #                 .participants \
    #                .create(messaging_binding_address='+1'+x)

message = client.conversations \
    .conversations('CHaca7ccf263504d7589898b02eee805b5') \
    .messages \
    .create(
         body='We found other users in CS 30700 with an open time slot to study @ 4:30-5:30 on Friday. Say Hi!',
         author='twilio'
     )

print(message.sid)

# print(client.conversations.
#     conversations(conversation.sid)
#     .delete())