from flask import Blueprint, render_template
from db.modele import db, User

views = Blueprint(__name__,"views")


@views.route("/")
def home():
    return render_template("index.html")

@views.route("/users") # do testowania, potem usunąć
def users():
    us = [u.to_dict() for u in User.query.all()]
    return render_template("users.html", users=us)

@views.route("/users/<int:user_id>") # też do testowania
def user(user_id):
    u = User.query.filter_by(id=user_id).first()
    return render_template("one_user.html", user=u)