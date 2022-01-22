# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
# create the application object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' # this is an arbitrary string
db = SQLAlchemy(app)

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
        if not verify_login():
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

def verify_login():
    return True

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('home'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
