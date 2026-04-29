# test code for first run
import os #maybe not needed?
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("login.html")
