from flask import Flask
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")


@app.route("/")
def index():
    return "test"

app.run(debug=True)
