# import the Flask class from the flask module
# from crypt import methods
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

# create the application object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' # this is an arbitrary string
db = SQLAlchemy(app)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            # flash stuff we don't care about
            return redirect(url_for('login'))
    return wrap


# class User(db.Model):
#     __tablename__ = "users"

#     uid = db.Integer()
#     phone_number = db


# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not verify_login(request.form['username'], request.form['password']):
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

def verify_login(username, password):
    return True

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('home'))

@app.route('/ical', methods=['GET','POST'])
@login_required # make sure user is authed
def get_ical():
    error=None
    if request.method == 'GET':
        # just display template
        return render_template('ical.html',error=error)
    elif request.method == 'POST':
        # get user's ical link
        link = request.form['icalurl']
        print(link)
        # imaginary_ical_func(link)
        # store users free time (presumably sql)
        # when they click submit, we want to redirect them to a confirmation page that gives them the group chat

@app.route('/confirm')
def confirm():
    pass

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)


