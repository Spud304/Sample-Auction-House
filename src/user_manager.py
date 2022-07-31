from models import db, User
from uuid import uuid4
from flask import Blueprint, jsonify, request
from json import loads


class UserBlueprint(Blueprint):
    def __init__(self):
        super().__init__("user", __name__)
        self.add_url_rule("/users/create", "create_user", self.create_user, methods=["POST"])
        self.add_url_rule("/users/<email>", "get_user", self.get_user, methods=["GET"])
        self.add_url_rule("/users", "get_users", self.get_users, methods=["GET"])

    def create_user(self):
        obj = loads(request.json)
        user = User(
            username=obj["username"],
            password=obj["password"],
            balance=0,
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    
    def get_user(self, email):
        query = db.session.query(User).filter(User.user_id == email)
        if query.count() == 0:
            return "User does not exist", 404
        user = query.first()
        return jsonify(user.to_dict()), 200
    
    def get_users(self):
        query = db.session.query(User)
        users = [user.to_dict() for user in query]
        return jsonify(users), 200