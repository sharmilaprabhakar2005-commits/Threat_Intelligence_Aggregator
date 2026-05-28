from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class IOC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    value = db.Column(db.String(255))
    source = db.Column(db.String(100))
    risk_score = db.Column(db.Integer)