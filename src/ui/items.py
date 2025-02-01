import json
import session_data
from flask import (
    render_template,
    session,
    Blueprint,
)
from bill.receipts import get_items, Items
from pathlib import Path
from logging import getLogger

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
    items = get_items(image_data)
    return items


@items_page.route("/items", methods=["GET"])
def list_items():
    items = get_current_items(session)
    items = items or get_test_items()
    items = items or get_receipt_image_items(session)
    save_items_file(items, session)

    return render_template("items.html", items=items.items)
