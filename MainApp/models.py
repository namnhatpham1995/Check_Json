# Models file contain models for the database
# classes' name and variables in the classes must match with the tables' name and columns inside tables
from datetime import datetime

from MainApp import db


class customer(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    active = db.Column(db.Boolean(1))

    def __init__(self, name, active):
        self.name = name
        self.active = active


class ip_blacklist(db.Model):
    ip = db.Column(db.String(255), primary_key=True)

    def __init__(self, ip):
        self.ip = ip


class ua_blacklist(db.Model):
    ua = db.Column(db.String(255), primary_key=True)

    def __init__(self, ua):
        self.ua = ua


class hourly_stats(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    customer_id = db.Column(db.String(255))
    time = db.Column(db.TIMESTAMP, index=True, default=datetime.utcnow)
    request_count = db.Column(db.BigInteger())
    invalid_count = db.Column(db.BigInteger())

    def __init__(self, customer_id, request_count, time, invalid_count):
        self.customer_id = customer_id
        self.request_count = request_count
        self.time = time
        self.invalid_count = invalid_count
