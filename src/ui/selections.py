import session_data
from flask import render_template, session, Blueprint, request
from bill.selections import get_item_selections
from logging import getLogger

log = getLogger(__file__)

selections_page = Blueprint("selections", __name__)


@selections_page.route("/selections", methods=["GET"])
def list_selections():
    no_selections = get_item_selections(session_data.get_receipt_items(session), [])
    person = request.form.get("person")
    selections = (
        session_data.get_person_selections(session, person) if person else no_selections
    )
    return render_template("selections.html", selections=selections)
