from flask import Flask
from items import items_page
from people import people_page
from selections import selections_page
from extras import extras_page
import os

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.register_blueprint(items_page)
app.register_blueprint(people_page)
app.register_blueprint(selections_page)
app.register_blueprint(extras_page)
