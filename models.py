from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# user
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100))
    password_hash = db.Column(db.String(255), nullable=False)
    reset_token = db.Column(db.String(255))
    username = db.Column(db.String(80), unique=True, nullable=False)


# painlog
class PainLog(db.Model):
    __tablename__ = "pain_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    pain_level = db.Column(db.Integer, nullable=False)
    pain_notes = db.Column(db.Text)
    body_view = db.Column(db.String(10))  # "front" or "back"
    body_areas = db.Column(db.Text)  # JSON string for now
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())