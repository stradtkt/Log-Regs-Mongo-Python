from flask import Flask, render_template, request, redirect, flash
from flask_pymongo import PyMongo
from pymongo import MongoClient

import datetime

app = Flask(__name__)
mongo = PyMongo(app)

# users = {
#   "name": "John Kellington", "city": "Cincinnati"
# }

# user = db['users'].insert_one(users)

client = MongoClient('mongodb://localhost:27017/')
db = client['app']
collection = db['users']


@app.route('/')
def index():
  users = collection.find()
  return render_template('index.html', users=users)


@app.route('/register_page')
def register_page():
  return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
  valid = True
  if request.form['email'] == "":
    valid = False
    flash("Email cannot be empty")
  if request.form['password'] == "":
    valid = False
    flash("Password cannot be empty")
  if request.form['name'] == "":
    valid = False
    flash("Name cannot be empty")
  if request.form['password'] != request.form['confirm_password']:
    valid = False
    flash("Your passwords need to match")
  if not valid:
    return redirect("/")
  else:
    record = {
      "name": request.form['name'],
      "email": request.form['email'],
      "username": request.form['username'],
      "password": request.form['password'],
      "created_at": datetime.datetime.now()
    }
    user = db['users'].insert_one(record)
    return redirect('/')
app.run(debug=True)