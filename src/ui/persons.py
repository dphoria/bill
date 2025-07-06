import json
import session_data
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


def save_persons_file(persons: list[Person], session):
    with open(
        session_data.session_item_path(session, session_data.PERSONS_FILE), "w"
    ) as json_file:
        json.dump([person.model_dump() for person in persons], json_file, indent=4)


def get_current_persons(session: dict) -> list[Person]:
    try:
        persons_file = session_data.session_item_path(
            session, session_data.PERSONS_FILE
        )
        if persons_file.exists():
            with open(persons_file, "r") as json_file:
                data = json.load(json_file)
                return [Person(**person_data) for person_data in data]
        return []
    except Exception as e:
        log.warning(f"Error reading persons file: {e}")
        return []


@persons_page.route("/persons", methods=["GET"])
def list_persons():
    persons = get_current_persons(session)
    return render_template("persons.html", persons=persons)


@persons_page.route("/persons", methods=["POST"])
def add_person():
    action = request.form.get("action")
    name = request.form.get("name", "").strip()

    # If name is provided, add the person
    if name:
        persons = get_current_persons(session)
        new_person = Person(name=name, items=[])
        persons.append(new_person)
        save_persons_file(persons, session)

    if action == "done":
        # Check if at least one person has been added
        persons = get_current_persons(session)
        if not persons:
            # If no persons added, stay on persons page
            return redirect(url_for("persons.list_persons"))
        # Redirect to items page when done and persons exist
        return redirect(url_for("items.list_items"))
    else:
        # Continue adding more persons
        return redirect(url_for("persons.list_persons"))
