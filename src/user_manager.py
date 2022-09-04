from src.models import db, User
from src.password_handler import PasswordHandler
from uuid import uuid4
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from json import loads


class UserBlueprint(Blueprint):
    def __init__(self):
        super().__init__("user", __name__)
        self.add_url_rule("/users/create", "create_user", self.create_user, methods=["POST"])
        self.add_url_rule("/users/<email>", "get_user", self.get_user, methods=["GET"]) # add auth header for this, so only the user can get their own user
        self.add_url_rule("/users", "get_users", self.get_users, methods=["GET"])
        self.add_url_rule("/users/credit/", "credit_user", self.credit_user, methods=["POST"]) # TODO: admin only
        self.add_url_rule("/profile", "profile", self.profile, methods=["GET"])

    @login_required
    def profile(self):
        return render_template("profile.html", name=current_user.username, balance=current_user.balance)

    def credit_user(self):
        """
        {
            "username": "",
            "amount": ""
        }
        """
        obj = loads(request.json)
        user = db.session.query(User).filter(User.username == obj["username"]).first()
        user.balance += obj["amount"]
        db.session.commit()
        d = {
            "username": user.username,
            "balance": user.balance,
        }
        return jsonify(d), 200

    def create_user(self):
        obj = loads(request.json)
        hashed_password = PasswordHandler().hash(obj["password"])
        user = User(
            username=obj["username"],
            email=obj["email"],
            password=hashed_password,
            balance=0,
        )
        db.session.add(user)
        db.session.commit()
        d = {
            "user_id": user.username,
            "balance": user.balance,
        }
        return jsonify(d), 201
    
    def get_user(self, email):
        query = db.session.query(User).filter(User.username == email)
        if query.count() == 0:
            return "User does not exist", 404
        user = query.first()
        d = {
            "user_id": user.username,
            "balance": user.balance,
        }
        return jsonify(d), 200
    
    def get_users(self):
        query = db.session.query(User)
        users = [user.__dict__ for user in query]
        return jsonify(users), 200