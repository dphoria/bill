import session_data
from flask import (
    render_template,
    session,
    Blueprint,
    request,
    jsonify,
)
from bill.receipts import Items, Item
from logging import getLogger
from items import get_current_items

log = getLogger(__file__)

extras_page = Blueprint("extras", __name__)


def get_default_extras() -> Items:
    """Return default extras: Service charge and Tax"""
    default_extras = [
        Item(name="Service charge", price=0.0),
        Item(name="Tax", price=0.0),
    ]
    return Items(items=default_extras)


def get_current_extras(session: dict) -> Items:
    extras = session_data.get_current_extras(session)
    return extras or get_default_extras()


@extras_page.route("/extras", methods=["GET"])
def list_extras():
    extras = get_current_extras(session)
    session_data.save_extras_file(extras, session)

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

    session_data.save_extras_file(extras, session)

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

    session_data.save_extras_file(extras, session)

    return jsonify({"success": True}), 200
