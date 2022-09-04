import re
from src.models import Listing, db, User
from uuid import uuid4
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from json import load, loads
from datetime import datetime as dt
from datetime import timedelta
from src.constants import TAX, DOWNPAYMENT


class ListingBlueprint(Blueprint):
    def __init__(self, name, import_name):
        super().__init__(name, import_name)
        self.add_url_rule('/listings/create', 'create_listing', self.create_listing)
        self.add_url_rule("/listings/create", "create_listing_post", self.create_listing_post, methods=["POST"])
        self.add_url_rule("/listings/<listing_id>", "buy_listing", self.buy_listing)
        self.add_url_rule("/listings/<listing_id>", "buy_listing_post", self.buy_listing_post, methods=["POST"])
        self.add_url_rule("/listings", "listings", self.get_top_listings, methods=["GET"])

        # self.add_url_rule("/listings/buy/<listing_id>", "buy_listing", self.buy_listing_post, methods=["POST"])
        


    @login_required
    def create_listing(self):
        return render_template("listing_creator.html")

    @login_required
    def create_listing_post(self):
        user = current_user
        if user.balance < int(request.form["buy_now"]) * DOWNPAYMENT:
            flash ("Not enough money")
            return redirect(url_for("listings.create_listing"))

        current_date = dt.now()
        formatted_date = current_date.strftime("%Y-%m-%d %H:%M")
        listing = Listing(
            name=request.form.get("item"),
            current_bid=0,
            highest_bidder=None,
            buy_now=request.form.get("buy_now"),
            seller=user.username,
            date_created=formatted_date
        )
        db.session.add(listing)
        user.balance -= int(request.form["buy_now"]) * DOWNPAYMENT
        db.session.commit()
        return redirect(url_for("index"))
    
    def buy_listing(self, listing_id):
        listing = db.session.query(Listing).filter(Listing.item_id == listing_id).first()
        return render_template("listing_view.html", listing=listing)

    def buy_listing_post(self, listing_id):
        if request.form.get("buy_button") == "buy":
            listing = db.session.query(Listing).filter(Listing.item_id == listing_id).first()
            user = current_user
            if user.balance < listing.buy_now:
                flash("Not enough money")
                return redirect(url_for("listings.buy_listing", listing_id=listing_id))
            if listing.current_bid >= listing.buy_now:
                flash("Someone has already bought this item")
                return redirect(url_for("listings.buy_listing", listing_id=listing_id))
            Listing.query.filter_by(item_id=listing_id).delete()
            user.balance -= listing.buy_now
            db.session.commit()
            return redirect(url_for("index"))

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
            time_left = dt.strptime(listing.date_created, "%Y-%m-%d %H:%M") + timedelta(hours=24) - dt.now()
            time_left = str(time_left).split(":")
            time_left = f"{time_left[0]} hours and {time_left[1]} minutes"
            a = {
                "item_name": listing.name,
                "item_id": listing.item_id,
                "current_bid": listing.current_bid,
                "highest_bidder": listing.highest_bidder,
                "buy_now": listing.buy_now,
                "seller": listing.seller,
                "date_created": listing.date_created,
                "time_left": time_left
            }
            l.append(a)
        return render_template("listings.html", listings=l)
