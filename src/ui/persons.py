from session_data import get_current_persons, save_persons_file
from flask import (
    render_template,
    session,
    Blueprint,
    request,
    redirect,
    url_for,
)
from bill.person import Person
from logging import getLogger

log = getLogger(__file__)

persons_page = Blueprint("persons", __name__)


@persons_page.route("/persons", methods=["GET"])
def list_persons():
    persons = get_current_persons(session)
    return render_template("persons.html", persons=persons)


@persons_page.route("/persons", methods=["POST"])
def add_person():
    action = request.form.get("action")
    name = request.form.get("name", "").strip()

    if name:
        persons = get_current_persons(session)
        new_person = Person(name=name, items=[])
        persons.append(new_person)
        save_persons_file(persons, session)

    if action == "done":
        persons = get_current_persons(session)
        if not persons:
            return redirect(url_for("persons.list_persons"))
        return redirect(url_for("items.list_items"))
    else:
        return redirect(url_for("persons.list_persons"))
