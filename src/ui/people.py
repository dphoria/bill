from flask import render_template, Blueprint, session, request, redirect, url_for
from logging import getLogger
import session_data

log = getLogger(__file__)

people_page = Blueprint("people", __name__)


@people_page.route("/people", methods=["GET"])
def list_people():
    return render_template("people.html", people=session_data.get_people(session))


@people_page.route("/people", methods=["POST"])
def add_person():
    person = request.form["name"]
    people = session_data.get_people(session) + [person]
    session_data.save_people(session, people)

    return redirect(url_for("people.list_people"))
