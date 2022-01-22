# import the Flask class from the flask module
# from crypt import methods
import sqlite3
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

# create the application object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' # this is an arbitrary string
app.database = "test.db"
# db = SQLAlchemy(app)

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
    return redirect(url_for('home'))

@app.route('/ical', methods=['GET','POST'])
@login_required # make sure user is authed
def ical():
    error=None
    if request.method == 'GET':
        # just display template
        return render_template('ical.html',error=error)
    elif request.method == 'POST':
        db = sqlite3.connect('test.db')
        cur = db.cursor()
        # get user's ical link
        link = request.form['icalurl']
        print(link)
        # store users free time (presumably sql)
        classes = retrieve_list_of_classes(link)
        for cid in classes:
            cur.execute("INSERT INTO enrolled (phone, class) VALUES (?, ?);",(session['phone'],cid))
        db.commit()
        db.close()
        # when they click submit, we want to redirect them to a confirmation page that gives them the group chat
        return redirect()

def retrieve_list_of_classes (icalurl) -> list:
    # assume we get it
    return ['CS 30700', 'CS 44800']


@app.route('/confirm')
def confirm():
    pass

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)

def retrieve_list_of_classes(icalurl) -> list:
    # assume we get it
    return ['CS 30700', 'CS 44800']


