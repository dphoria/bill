from flask import Flask
from items import items_page
from persons import persons_page
from distribute import distribute_page
from extras import extras_page
from payments import payments_page
import os

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.register_blueprint(items_page)
app.register_blueprint(persons_page)
app.register_blueprint(distribute_page)
app.register_blueprint(extras_page)
app.register_blueprint(payments_page)
