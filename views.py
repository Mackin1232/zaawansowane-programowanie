from flask import Blueprint, render_template
from db.modele import User

views = Blueprint(__name__,"views")


@views.route("/")
def home():
    return render_template("index.html")

@views.route("/users")
def users():
    us = User.all_users()
    return render_template("users.html", users=us)

@views.route("/users/<int:user_id>")
def user(user_id):
    u = User.search_user(user_id)
    return render_template("one_user.html", user=u)