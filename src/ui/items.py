import json
import os
import constants
from flask import render_template, session, Blueprint, request, redirect, url_for
from bill.receipts import get_items, Items, Item
from pathlib import Path
from logging import getLogger
from pydantic import TypeAdapter

log = getLogger(__file__)

items_page = Blueprint("items", __name__)


def read_items_file(items_file_path: os.PathLike) -> Items:
    return Items.model_validate_json(json.loads(Path(items_file_path).read_text()))


def save_items_file(items: Items, session):
    with open(
        constants.session_item_path(session, constants.ITEMS_FILE), "w"
    ) as json_file:
        json.dump(items.model_dump_json(indent=4), json_file)


def get_test_items() -> Items | None:
    try:
        json_file = Path(__file__).parent / "test_items.json"
        items = read_items_file(json_file)
        return items if any(items.items) else None
    except Exception as e:
        log.debug(f"Error while reading {json_file}: {e}")
        return None


def get_current_items(session) -> Items | None:
    try:
        return read_items_file(
            constants.session_item_path(session, constants.ITEMS_FILE)
        )
    except Exception as e:
        log.warning(f"current list of items is empty: {e}")
        return None


def get_receipt_image_items(session) -> Items:
    image_file_path = constants.session_item_path(session, constants.IMAGE_FILE)
    image_data = Path(image_file_path).read_bytes()
    items = get_items(image_data)
    return items


@items_page.route("/items", methods=["GET"])
def list_items():
    items = get_current_items(session)
    items = items or get_test_items()
    items = items or get_receipt_image_items(session)
    save_items_file(items, session)

    return render_template("items.html", items=items.items)


@items_page.route("/items", methods=["POST"])
def add_item():
    try:
        new_item = TypeAdapter(Item).validate_python(
            {
                "name": request.form["name"],
                "count": request.form["count"],
                "price": request.form["price"],
            }
        )
    except Exception as e:
        log.error(str(e))
    else:
        items = get_current_items(session)
        items.items.append(new_item)
        save_items_file(items, session)

    return redirect(url_for("items.list_items"))


@items_page.route("/items/next", methods=["POST"])
def save_items():
    table_data = request.form.get("table_data")
    items_json = json.loads(table_data)
    items_list = map(TypeAdapter(Item).validate_python, items_json)
    items = Items(items=list(items_list))
    save_items_file(items, session)

    log.info(str(items))

    return redirect(url_for("people.list_people"))
