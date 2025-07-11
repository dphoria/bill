import json
import session_data
from flask import (
    render_template,
    session,
    Blueprint,
    request,
    jsonify,
)
from bill.receipts import Items, Item
from pathlib import Path
from logging import getLogger
from items import get_current_items

log = getLogger(__file__)

extras_page = Blueprint("extras", __name__)


def save_extras_file(extras: Items, session):
    with open(
        session_data.session_item_path(session, session_data.EXTRAS_FILE), "w"
    ) as json_file:
        json.dump(extras.model_dump_json(indent=4), json_file)


def get_default_extras() -> Items:
    """Return default extras: Service charge and Tax"""
    default_extras = [
        Item(name="Service charge", price=0.0),
        Item(name="Tax", price=0.0),
    ]
    return Items(items=default_extras)


def get_current_extras(session: dict) -> Items | None:
    try:
        extras_file = session_data.session_item_path(session, session_data.EXTRAS_FILE)
        if Path(extras_file).exists():
            return session_data.read_items_file(extras_file)
        else:
            return get_default_extras()
    except Exception as e:
        log.warning(f"current list of extras is empty: {e}")
        return get_default_extras()


@extras_page.route("/extras", methods=["GET"])
def list_extras():
    extras = get_current_extras(session)
    save_extras_file(extras, session)

    items = get_current_items(session)
    items_total = items.get_sum()

    return render_template("extras.html", extras=extras.items, items_total=items_total)


@extras_page.route("/add_extra", methods=["POST"])
def add_extra():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")

    extras = get_current_extras(session)

    new_extra = Item(name=name, price=price)
    extras.items.append(new_extra)

    save_extras_file(extras, session)

    return jsonify({"success": True}), 200


@extras_page.route("/update_extra", methods=["POST"])
def update_extra():
    data = request.get_json()
    extra_index = data.get("extra_index")
    name = data.get("name")
    price = data.get("price")

    extras = get_current_extras(session)

    extras.items[extra_index].name = name
    extras.items[extra_index].price = price

    save_extras_file(extras, session)

    return jsonify({"success": True}), 200
