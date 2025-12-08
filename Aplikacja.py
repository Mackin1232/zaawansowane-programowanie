from flask import Flask
from views import views
from config import Config
from db.modele import db, User
from sample_data import load_data

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

app.config.from_object(Config)

db.init_app(app)
load_data(app)

@app.route("/")
def index():
    return "test"

@app.route("/users")
def users():
    return User.all_users()

app.run(debug=True)
