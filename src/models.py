from __future__ import annotations
from dataclasses import dataclass
from email.policy import default
from uuid import uuid4
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Listing(db.Model):
    __tablename__ = 'listings'
    name = Column(String)
    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    current_bid = Column(Integer)
    highest_bidder = Column(String)
    buy_now = Column(Integer)
    seller = Column(String)
    date_created = Column(String)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    balance = Column(Integer)