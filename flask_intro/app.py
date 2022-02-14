# import the Flask class from the flask module
# from crypt import methods
import logging
import sqlite3
from tkinter import READABLE
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import icalparser as ip

# create the application object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' # this is an arbitrary string
app.database = "test.db"
# db = SQLAlchemy(app)
TIMES = ['700', '750', '800', '850', '900', '950', '1000', '1050', '1100', '1150', '1200', '1250', '1300', '1350', '1400', '1450', '1500', '1550', '1600', '1650', '1700', '1750', '1800', '1850', '1900', '1950', '2000', '2050']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
READABLE_TIME = {'700': "7:00AM", '750': "7:30AM", '800':"8:00AM", '850':"8:30AM", '900':"9:00AM", '950':"9:30AM", '1000':"10:00AM", '1050':"10:30AM", '1100':"11:00AM", '1150':"11:30AM", '1200':"12:00PM", '1250':"12:30AM", '1300':"1:00PM", '1350':"1:30PM", 
        '1400':"2:00PM", '1450':"2:30PM", '1500':"3:00PM", '1550':"3:30PM", '1600':"4:00PM", '1650':"4:30", '1700':"5:00PM", '1750':"5:30PM", '1800':"6:00PM", '1850':"6:30PM", '1900':0, '1950':"7:00PM", '2000':"8:00PM", '2050':"8:30PM"}
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            # flash stuff we don't care about
            return redirect(url_for('login'))
    return wrap

# not using sqlalchemy as of 3pm
# class User(db.Model):
#     __tablename__ = "users"

#     uid = db.Integer()
#     phone_number = db.String()



# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not verify_login(request.form['phone']):
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            session['phone'] = request.form['phone']
            return redirect(url_for('ical'))
    return render_template('login.html', error=error)

def verify_login(phonenum):
    return True

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('login'))

# d.execute("CREATE TABLE enrolled (phone TEXT NOT NULL, class TEXT NOT NULL, PRIMARY KEY(phone,class));")
# for day in days:                                          
#     cur.execute(f'CREATE TABLE {day} (phone TEXT NOT NULL);')
# for day in days:                               
#     for time in times_str:
#             cur.execute(f'ALTER TABLE {day} ADD COLUMN \"{time}\" INTEGER NOT NULL;')
@app.route('/ical', methods=['GET','POST'])
@login_required # make sure user is authed
def ical():
    error=None
    if request.method == 'GET':
        # just display template
        return render_template('ical.html',error=error)
    elif request.method == 'POST':
        # get user's ical link
        link = request.form['icalurl']
        print(link)

        db = sqlite3.connect('test.db')
        cur = db.cursor()
        # store users free time (presumably sql)
        classes = retrieve_list_of_classes(link)
        for cid in classes:
            try:
                cur.execute("INSERT INTO enrolled (phone, class) VALUES (?, ?);",(session['phone'],cid))
            except sqlite3.IntegrityError:
                logging.warning(f"Can't reuse same phonum {session['phone']}, class {cid}")
                return render_template('ical.html', error="Can't reuse the same phone number, try again?")
        # ical procedures will return 5 dicts, one for each day.
        day_timeslots = ip.get_timeslots(ip.get_ics(link))
        insert_into(day_timeslots, cur) # large repetitive sql operation

        db.commit()
        db.close()
        # when they click submit, we want to redirect them to a confirmation page that gives them the group chat
        return redirect(url_for('confirm'))
def insert_single_table(phone, day_value_list):
    pass
def insert_into(day_timeslots, cur):
        mon = [session['phone']]
        mon += retrieve_list_of_timeslots(day_timeslots[0])
        # 29 ?s because 28 half hours + 1 phone num.
        cur.execute("INSERT INTO Monday VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", mon)

        tues = [session['phone']]
        tues += retrieve_list_of_timeslots(day_timeslots[1])
        # 29 ?s because 28 half hours + 1 phone num.
        cur.execute("INSERT INTO Tuesday VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", tues)

        wed = [session['phone']]
        wed += retrieve_list_of_timeslots(day_timeslots[2])
        # 29 ?s because 28 half hours + 1 phone num.
        cur.execute("INSERT INTO Wednesday VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", wed)

        thurs = [session['phone']]
        thurs += retrieve_list_of_timeslots(day_timeslots[3])
        # 29 ?s because 28 half hours + 1 phone num.
        cur.execute("INSERT INTO Thursday VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", thurs)

        fri = [session['phone']]
        fri += retrieve_list_of_timeslots(day_timeslots[4])
        # 29 ?s because 28 half hours + 1 phone num.
        cur.execute("INSERT INTO Friday VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", fri)

def retrieve_list_of_classes (icalurl) -> set:
    # assume we get it
    cal = ip.get_ics(icalurl)
    return ip.get_classes(cal)
def retrieve_list_of_timeslots(daydict) -> list:
    slots = []
    for i in TIMES:
        slots.append(daydict[i]) # ensures order is preserved
    return slots


@app.route('/confirm')
def confirm():
    # check if the user
    session['phone']
    # has good enough free sections to text
    if True: # assume good enough
        class_list = create_class_list
        con = sqlite3.connect('test.db')
        too_many_slots = get_same_timeslot(con)
        determine_study_time_frame()
    return render_template('confirm.html',error=None)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)

def retrieve_list_of_classes(icalurl) -> list:
    # assume we get it
    return ['CS 30700', 'CS 44800']

conn = sqlite3.connect('test.db')

def create_class_list(conn) -> dict():
    cur = conn.cursor()
    cur.execute("SELECT * FROM enrolled")

    rows = cur.fetchall()
    class_list = dict()
    
    for row in rows:
        if row[1] not in class_list:
            class_list[row[1]] = row[0]
        else:
            class_list[row[1]] = class_list[row[1]] + "," + row[0]

    return class_list

def get_same_timeslot(conn) -> dict:
    class_list = create_class_list(conn)
    cur = conn.cursor()

    for i in class_list:
        print(i)
        slots = {'700':0, '750':0, '800':0, '850':0, '900':0, '950':0, '1000':0, '1050':0, '1100':0, '1150':0, '1200':0, '1250':0, '1300':0, '1350':0, 
        '1400':0, '1450':0, '1500':0, '1550':0, '1600':0, '1650':0, '1700':0, '1750':0, '1800':0, '1850':0, '1900':0, '1950':0, '2000':0, '2050':0}
        
        please = list()
        print(class_list[i])
        for phone in class_list[i].split(','):
            cur.execute("SELECT * FROM Monday WHERE phone=?", (phone,))
            rows = cur.fetchall()
            please.append(rows)
        # Find study time slots
        for slot in range(1, 29):
            value = 0
            for tuples in please:
                for user in tuples:
                    value+=int(user[slot])

            if value == 0:
                slots[TIMES[slot - 1]] = 0
            else:
                slots[TIMES[slot - 1]] = 1

        # print(please)
        print (slots)
        determine_study_time_frame(slots, "lol")

def determine_study_time_frame(slots, day) -> list():
    start = 0
    end = 0
    frames = list()
    for interval in TIMES:
        if slots[interval] == 0  and start == 0:
            start = interval
        elif start != 0 and (slots[interval] == 1 or interval == TIMES[-1]):
            end = interval

        if end != 0:
            frames.append((READABLE_TIME[start], READABLE_TIME[end]))
            start = end = 0
    print(frames)

def send_twilio(phone_list, frames) -> None:
                
            

    create_class_list(conn)
    get_same_timeslot(conn)

# def send_twilio(["6147023950", "6147023950","6147023950"], abritrary_string):
#     # send arbitrary_string

