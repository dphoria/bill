from flask import render_template, Blueprint
from logging import getLogger

log = getLogger(__file__)

people_page = Blueprint("people", __name__)


@people_page.route("/people", methods=["GET"])
def list_people():
    return render_template("people.html", people=[])


@people_page.route("/people", methods=["POST"])
def add_person():
    pass
