import json
import session_data
from flask import render_template, session, Blueprint, request
from logging import getLogger

log = getLogger(__file__)

selections_page = Blueprint("selections", __name__)


def list_selections(session, people, person_index):
    selections = session_data.get_person_selections(session, people[person_index])
    return render_template(
        "selections.html",
        people=people,
        selections=selections,
        person_index=person_index,
        tax_percent=session[session_data.TAX_PERCENT],
        tip_percent=session[session_data.TIP_PERCENT],
    )


@selections_page.route("/selections", methods=["GET"])
def home():
    people = session_data.get_people(session)
    session[session_data.CURRENT_PERSON] = people[0]
    return list_selections(session, people, 0)


def save_person_selections(session, person: str, selected_items: list[int]):
    selections_file = session_data.session_item_path(
        session, session_data.SELECTIONS_FILE
    )

    try:
        selections = json.loads(selections_file.read_text())
    except FileNotFoundError:
        log.debug(f"{session_data.SELECTIONS_FILE} not found")
        selections = {}

    log.info(f"{person} : {selected_items}")
    selections[person] = selected_items
    selections_file.write_text(json.dumps(selections))


@selections_page.route("/selections", methods=["POST"])
def save_selections():
    save_person_selections(
        session,
        session[session_data.CURRENT_PERSON],
        json.loads(request.form["selected-items"]),
    )

    person = request.form["selected-person"]
    session[session_data.CURRENT_PERSON] = person
    people = session_data.get_people(session)

    return list_selections(session, people, people.index(person))
