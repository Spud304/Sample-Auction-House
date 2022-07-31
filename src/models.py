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

    def __init__(self, name, item_id, current_bid, highest_bidder, buy_now, seller):
        self.name = name
        self.item_id = item_id
        self.current_bid = current_bid
        self.highest_bidder = highest_bidder
        self.buy_now = buy_now
        self.seller = seller

    def __repr__(self):
        return f'<Listing {self.item_id}>'



# mapper_registry = registry()

# @mapper_registry.mapped
# @dataclass
# class Listing():
#     def __init__(self, name, price, item_id, current_bid, highest_bidder, buy_now, seller):
#         self.name = name
#         self.price = price
#         self.item_id = item_id
#         self.current_bid = current_bid
#         self.highest_bidder = highest_bidder
#         self.buy_now = buy_now
#         self.seller = seller


#     __table__ = Table(
#         "listings",
#         mapper_registry.metadata,
#         Column("name", String(100), nullable=False),
#         Column("price", Integer, nullable=False),
#         Column("item_id", String(36), primary_key=True, default=uuid4),
#         Column("current_bid", Integer, nullable=False),
#         Column("highest_bidder", String(36), nullable=True, default=uuid4),
#         Column("buy_now", Integer, nullable=False),
#         Column("seller", String(36), nullable=False, default=uuid4)
#     )
#     name: str = field(init=False)
#     price: int = field(init=False)
#     item_id: uuid4 = field(init=False)
#     current_bid: int = field(init=False)
#     highest_bidder: uuid4 = field(init=False)
#     buy_now: int = field(init=False)
#     seller: uuid4 = field(init=False)