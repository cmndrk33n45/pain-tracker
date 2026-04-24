# test code for first run
import os #maybe not needed?
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

@app.route("/")
def home():
    return "Pain Tracker App is running"

app.run(debug=True)