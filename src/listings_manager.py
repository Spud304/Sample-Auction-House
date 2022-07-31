from models import Listing, db
from uuid import uuid4
from flask import Blueprint, jsonify, request
from json import loads


class ListingBlueprint(Blueprint):
    def __init__(self, name, import_name):
        super().__init__(name, import_name)
        self.add_url_rule("/listings/create", "create_listing", self.create_listing, methods=["POST"])
        self.add_url_rule("/listings/<user_id>", "get_user_listings", self.get_user_listings, methods=["GET"])
        self.add_url_rule("/listings/buy/<listing_id>", "buy_listing", self.buy_listing, methods=["POST"])
        self.add_url_rule("/listings", "get_listings", self.get_top_listings, methods=["GET"])

    def create_listing(self):
        print(request.json)
        obj = loads(request.json)
        listing = Listing(
            name=obj["name"],
            item_id=obj["item_id"],
            current_bid=0,
            highest_bidder=None,
            buy_now=obj["buy_now"],
            seller=obj["seller"]
        )
        db.session.add(listing)
        db.session.commit()
        print(listing)
        return "Listing created", 201
    
    def buy_listing(self, listing_id):
        # buy a listing, if the price is less than the buy now price, then update the highest bidder and current bid
        # if the money is the buy now price then remove the listing from the database
        # if the listing does not exist, or money is higher than buy_now, return a 404

        query = db.session.query(Listing).filter(Listing.item_id == listing_id)
        if query.count() == 0:
            return "Listing does not exist", 404
        listing = query.first()
        obj = loads(request.json)
        print(f'Request price {obj["money"]}, current bid {listing.current_bid}')
        if obj["money"] == listing.buy_now:
            db.session.delete(listing)
            db.session.commit()
            return "Listing bought", 200
        elif obj["money"] < listing.buy_now and obj["money"] > listing.current_bid:
            listing.highest_bidder = obj["user_id"]
            listing.current_bid = obj["money"]
            db.session.commit()
            print(f'Listing has been updated to {listing.current_bid}')
            return "Listing updated", 200
        elif obj["money"] <= listing.current_bid:
            return "Not enough money", 400
        
        return "Listing does not exist", 404

    def get_user_listings(self, user_id):
        # get all listings for a user
        query = db.session.query(Listing).filter(Listing.seller == user_id)
        l = []
        for listing in query:
            print(listing)
            a = {
                "name": listing.name,
                "item_id": listing.item_id,
                "current_bid": listing.current_bid,
                "highest_bidder": listing.highest_bidder,
                "buy_now": listing.buy_now,
                "seller": listing.seller
            }
            l.append(a)
        print(l)
        return jsonify(l), 201
    
    def get_top_listings(self):
        # get top 10 listings with highest bid
        query = db.session.query(Listing).order_by(Listing.current_bid.desc()).limit(10)
        l = []
        for listing in query:
            a = {
                "name": listing.name,
                "item_id": listing.item_id,
                "current_bid": listing.current_bid,
                "highest_bidder": listing.highest_bidder,
                "buy_now": listing.buy_now,
                "seller": listing.seller
            }
            l.append(a)
        return jsonify(l), 201
