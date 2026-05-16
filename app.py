# test code for first run
import os #maybe not needed?
from datetime import date, datetime
from flask import Flask, render_template, session, g, request, redirect, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from models import db, User, PainLog
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db.init_app(app)

# create / enable rows
with app.app_context():
    db.create_all()

# login required decorator
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
    user = User.query.get(session["user_id"])
    return render_template("dashboard.html", user=user)
    

@app.route("/log_pain", methods=["GET", "POST"])
@login_required
def log_pain():
    user = User.query.get(session["user_id"])
    errors = {}

    if request.method == "POST":
        pain_level = request.form.get("pain_level")
        pain_notes = request.form.get("pain_notes")

        if not pain_level:
            errors["pain_level"] = True
            return render_template("log_pain.html", user=user, errors=errors)

        pain_level = int(pain_level)
        today = date.today()

        existing_log = PainLog.query.filter(
            PainLog.user_id == user.id,
            db.extract("year", PainLog.created_at) == today.year,
            db.extract("month", PainLog.created_at) == today.month,
            db.extract("day", PainLog.created_at) == today.day
        ).first()

        if existing_log:
            existing_log.pain_level = pain_level
            existing_log.pain_notes = pain_notes
        else:
            pain_log = PainLog(
                user_id=user.id,
                pain_level=pain_level,
                pain_notes=pain_notes
            )
            db.session.add(pain_log)

        db.session.commit()
        return redirect("/")

    return render_template("log_pain.html", user=user, errors=errors)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    # check if form was submitted, otherwise provide the site.
    errors = {}
    
    if request.method == "POST":
        #get the values from the form
        username = request.form.get("username")
        password = request.form.get("password") 

        # make sure are feilds were filled
        if not username:
            errors["username_missing"] = True
        if not password:
            errors["password_missing"] = True
        
        # if any of those feilds were no filled out, send back to the login route and highlight incorrect forms.
        if errors: 
            return render_template("login.html", errors=errors)
        else:
            # get user from db
            user = User.query.filter_by(username=username).first()

            # check if user exists, if not 
            if not user or not check_password_hash(user.password_hash, password):
                errors["wrong_info"] = True
                return render_template("login.html", errors={"": True})
            else:
                session["user_id"] = user.id
                return redirect("/")
    else:
        return render_template("login.html", errors=errors)
    

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/pain_log", methods=["GET"])
@login_required
def pain_log():
    user = User.query.get(session["user_id"])
    selected_range = request.args.get("range", "month")
    query = PainLog.query.filter_by(user_id=user.id)
    pain = query.order_by(PainLog.created_at.asc()).all()
    labels = [log.created_at.strftime("%Y-%m-%d") for log in pain]
    title = "All Time"

    today = date.today()

    if selected_range == "month":
        labels = [
            log.created_at.strftime("%d")
            for log in pain
        ]   
        title = today.strftime("%B")
        query = query.filter(
            db.extract("year", PainLog.created_at) == today.year,
            db.extract("month", PainLog.created_at) == today.month
        )

    elif selected_range == "year":
        labels = [
            log.created_at.strftime("%b")
            for log in pain
        ]
        title = str(today.year)
        query = query.filter(
            db.extract("year", PainLog.created_at) == today.year
        )


    pain_levels = [log.pain_level for log in pain]

    return render_template(
        "pain_log.html",
        pain=pain,
        labels=labels,
        pain_levels=pain_levels,
        selected_range=selected_range,
        title=title
    )


@app.route("/report", methods=["GET", "POST"])
def report():
    return redirect("/")


@app.route("/settings", methods=["GET", "POST"])
def settings():
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    errors = {}
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username:
            errors["username"] = True
        if not email:
            errors["email"] = True
        if not password:
            errors["password"] = True
        if not confirm_password:
            errors["confirm_password"] = True

        # if a field is missing, display errors,  
        if errors:
            return render_template("signup.html", errors=errors)
        # if the passwords do not match
        elif password != confirm_password:
            errors["password_mismatch"] = True
            return render_template("signup.html", errors=errors)
        else:
            # get user from db
            user = User.query.filter_by(username=username).first()

            # check see if user exists
            if user is None:
                new_user = User(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash(password, method="pbkdf2:sha256")
                )

                db.session.add(new_user)
                db.session.commit()

                session["user_id"] = new_user.id
                return redirect("/")                
            else:
                return render_template("signup.html", errors=errors)
    else:
        return render_template("signup.html", errors=errors)