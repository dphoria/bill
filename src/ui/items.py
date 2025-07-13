import json
import session_data
from flask import (
    render_template,
    session,
    Blueprint,
    request,
    jsonify,
)
from bill.receipts import Receipt, Items, Item
from pathlib import Path
from logging import getLogger
from persons import get_current_persons, save_persons_file

log = getLogger(__file__)

items_page = Blueprint("items", __name__)


def save_items_file(items: Items, session):
    with open(
        session_data.session_item_path(session, session_data.ITEMS_FILE), "w"
    ) as json_file:
        json.dump(items.model_dump_json(indent=4), json_file)


def get_test_items() -> Items | None:
    try:
        json_file = Path(__file__).parent / "test_items.json"
        items = session_data.read_items_file(json_file)
        return items if any(items.items) else None
    except Exception as e:
        log.debug(f"Error while reading {json_file}: {e}")
        return None


def get_current_items(session: dict) -> Items | None:
    try:
        return session_data.get_receipt_items(session)
    except Exception as e:
        log.warning(f"current list of items is empty: {e}")
        return None


def get_receipt_image_items(session: dict) -> Items:
    image_file_path = session_data.session_item_path(session, session_data.IMAGE_FILE)
    image_data = Path(image_file_path).read_bytes()
    receipt = Receipt(image_data)
    items = receipt.get_items()
    return items


@items_page.route("/items", methods=["GET"])
def list_items():
    items = get_current_items(session)
    items = items or get_test_items()
    items = items or get_receipt_image_items(session)
    save_items_file(items, session)

    return render_template("items.html", items=items.items)


@items_page.route("/get_persons", methods=["GET"])
def get_persons():
    persons = get_current_persons(session)
    return jsonify([person.model_dump() for person in persons]), 200


@items_page.route("/add_item", methods=["POST"])
def add_item():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")

    items = get_current_items(session)

    new_item = Item(name=name, price=price)
    items.items.append(new_item)

    save_items_file(items, session)

    return jsonify({"success": True}), 200


@items_page.route("/update_item", methods=["POST"])
def update_item():
    data = request.get_json()
    item_index = data.get("item_index")
    name = data.get("name")
    price = data.get("price")

    items = get_current_items(session)
    items.items[item_index].name = name
    items.items[item_index].price = price

    save_items_file(items, session)

    return jsonify({"success": True}), 200


@items_page.route("/split_item", methods=["POST"])
def split_item():
    data = request.get_json()
    item_index = data.get("item_index")

    items = get_current_items(session)
    items.split(item_index)
    save_items_file(items, session)

    return jsonify({"success": True}), 200


@items_page.route("/prepare_split", methods=["POST"])
def prepare_split():
    items = get_current_items(session)
    item_count = len(items.items)
    persons = get_current_persons(session)

    persons_items = map(lambda person: set(person.items), persons)
    all_shared_items = set.union(*persons_items)
    unshared_items = set(range(item_count)) - all_shared_items

    if unshared_items:
        for person in persons:
            person.items = sorted(set(person.items + list(unshared_items)))

        save_persons_file(persons, session)

    return (
        jsonify(
            {
                "success": True,
                "item_count": item_count,
                "person_count": len(persons),
            }
        ),
        200,
    )
