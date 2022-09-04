from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import registry
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Listing(db.Model):
    __tablename__ = 'listings'
    name = Column(String)
    item_id = Column(String, primary_key=True)
    current_bid = Column(Integer)
    highest_bidder = Column(String)
    buy_now = Column(Integer)
    seller = Column(String)
    date_created = Column(String)

    def __init__(self, name, item_id, current_bid, highest_bidder, buy_now, seller, date_created):
        self.name = name
        self.item_id = item_id
        self.current_bid = current_bid
        self.highest_bidder = highest_bidder
        self.buy_now = buy_now
        self.seller = seller
        self.date_created = date_created

    def __repr__(self):
        return f'<Listing {self.item_id}>'

class User(db.Model):
    __tablename__ = 'users'
    id_ = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    balance = Column(Integer)

    # def __init__(self, username, email, password, balance, id_):
    #     self.id_ = id_
    #     self.username = username
    #     self.email = email
    #     self.password = password
    #     self.balance = balance

    def __repr__(self):
        return f'<User {self.username}>'