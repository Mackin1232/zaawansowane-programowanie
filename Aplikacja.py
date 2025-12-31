from flask import Flask, render_template
from views import views
from config import Config
from db.modele import db, User
from laduj_dane import load_data


app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

app.config.from_object(Config)

db.init_app(app)
load_data(app)

@app.route("/")
def index():
    return "test"

app.run(debug=True)

