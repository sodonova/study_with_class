import os
from pydoc import cli
from twilio.rest import Client

phonenum = [ "6147023950", "3172497574","9148067766", "7658389656"]


# Your Account SID from twilio.com/console
account_sid = "ACf34a7eb9833912a41f4dc2f2c76dd6b1"
# Your Auth Token from twilio.com/console
auth_token  = "1c35356d92d60326c491a2d896aa30c5"

client = Client(account_sid, auth_token)


conv_sid = "CHc2488446a87b40948e3312cac8eb3b24"

# (venv) PS C:\Users\sean1\Documents\3Y\bmIX\study_with_class> python
# Python 3.9.5 (tags/v3.9.5:0a7dcbd, May  3 2021, 17:27:52) [MSC v.1928 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license" for more information.
# >>> from msg_min import *  
# >>> conv = client.conversations.conversations(conv_sid)                         
# >>> message = client.conversations.conversations(conv_sid).messages.create(body='ligma',author='twilio')
# >>> message.sid
# 'IM48dc9a0063464daf83d90bebe7705993'
# >>>