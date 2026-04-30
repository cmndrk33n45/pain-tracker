# test code for first run
import os #maybe not needed?
from flask import Flask, render_template, session, g, request, redirect, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

db = SQLAlchemy(app)

#helper functions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
@login_required
def home():
    return render_template("dashboard.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")