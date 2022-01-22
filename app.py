from crypt import methods
from urllib import request
from flask import Flask
import sqlite3

app = Flask(__name__)


@app.route('/signin',methods=['POST'])
def hello():
    request.args.email
    return 'Hello, World!'

def handle_ical_url(url):
    pass
def send_twilio_message(numberArray):
    pass
