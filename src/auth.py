from src.models import db, User
from src.password_handler import PasswordHandler
from uuid import uuid4
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from json import loads
from flask_login import login_user, login_required, logout_user

class AuthBlueprint(Blueprint):
    def __init__(self):
        super().__init__("auth", __name__)
        self.add_url_rule("/login", "login", self.login)
        self.add_url_rule("/login", "login_post", self.login_post, methods=["POST"])
        self.add_url_rule("/signup", "signup", self.signup)
        self.add_url_rule("/signup", "signup_post", self.signup_post, methods=["POST"])
        self.add_url_rule("/logout", "logout", self.logout)

    def login(self):
        return render_template("login.html")

    def login_post(self):
        # login code goes here
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not PasswordHandler.verify(user.password, password, user.password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('user.profile'))

    def signup(self):
        return render_template("signup.html")

    def signup_post(self):
        email = request.form.get('email')
        username = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        
        hashed_password = PasswordHandler().hash(password)
        new_user = User(email=email, username=username, password=hashed_password, balance=0)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    
    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('index'))