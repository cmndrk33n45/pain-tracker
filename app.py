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
app.config["SESSION_TYPE"] = "filesystem"
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
    # check if form was submitted, otherwise provide the site.
    if request.method == "POST":
        # make sure are feilds were filled
        errors = {}
        if not request.form.get("username"):
            errors["username"] = False
        if not request.form.get("email"):
            errors["email"] = False
        if not request.form.get("password"):
            errors["password"] = False
        
        # if any of those feilds were no filled out, send back to the login route and highlight incorrect forms.
        if errors: 
            return render_template("login.html", errors=errors)
        else:
            i = 0
    else:
        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        i = 0
    else:
        return render_template("signup.html")