from flask import Flask
from items import items_page
import os

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.register_blueprint(items_page)
