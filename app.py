# test code for first run
import os #maybe not needed?
from flask import Flask, render_template, session, g, request, redirect, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQLAlchemy(app)

# helper functions:

# create SQL classes
# user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100))
    password_hash = db.Column(db.String(255), nullable=False)
    reset_token = db.Column(db.String(255))
    username = db.Column(db.String(80), unique=True, nullable=False)

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