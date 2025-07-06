import json
import session_data
from flask import (
    render_template,
    session,
    Blueprint,
    request,
    jsonify,
)
from bill.receipts import get_items, Items, Item
from pathlib import Path
from logging import getLogger
from .persons import get_current_persons, save_persons_file

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


@items_page.route("/get_persons", methods=["GET"])
def get_persons():
    try:
        persons = get_current_persons(session)
        return jsonify([person.model_dump() for person in persons]), 200
    except Exception as e:
        log.error(f"Error getting persons: {e}")
        return jsonify({"error": "Internal server error"}), 500


@items_page.route("/add_item", methods=["POST"])
def add_item():
    try:
        data = request.get_json()
        name = data.get("name")
        price = data.get("price")

        # Get current items
        items = get_current_items(session)
        if not items:
            # Create new items list if none exists
            items = Items(items=[])

        # Create new item
        new_item = Item(name=name, price=price)
        items.items.append(new_item)

        # Save updated items
        save_items_file(items, session)

        return jsonify({"success": True}), 200

    except Exception as e:
        log.error(f"Error adding item: {e}")
        return jsonify({"error": "Internal server error"}), 500


@items_page.route("/update_item", methods=["POST"])
def update_item():
    try:
        data = request.get_json()
        item_index = data.get("item_index")
        name = data.get("name")
        price = data.get("price")

        if item_index is None or name is None or price is None:
            return jsonify({"error": "Missing required fields"}), 400

        # Get current items
        items = get_current_items(session)
        if not items:
            return jsonify({"error": "No items found"}), 404

        # Validate item index
        if item_index < 0 or item_index >= len(items.items):
            return jsonify({"error": "Invalid item index"}), 400

        # Update the item
        items.items[item_index].name = name
        items.items[item_index].price = price

        # Save updated items
        save_items_file(items, session)

        return jsonify({"success": True}), 200

    except Exception as e:
        log.error(f"Error updating item: {e}")
        return jsonify({"error": "Internal server error"}), 500


@items_page.route("/split_item", methods=["POST"])
def split_item():
    try:
        data = request.get_json()
        item_index = data.get("item_index")

        if item_index is None:
            return jsonify({"error": "Missing item index"}), 400

        # Get current items
        items = get_current_items(session)
        if not items:
            return jsonify({"error": "No items found"}), 404

        # Validate item index
        if item_index < 0 or item_index >= len(items.items):
            return jsonify({"error": "Invalid item index"}), 400

        # Get the item to split
        original_item = items.items[item_index]

        # Create two new items with half the price each
        item1 = Item(name=f"{original_item.name} (1/2)", price=original_item.price / 2)
        item2 = Item(name=f"{original_item.name} (2/2)", price=original_item.price / 2)

        # Replace the original item with the first split item
        items.items[item_index] = item1

        # Insert the second split item after the first
        items.items.insert(item_index + 1, item2)

        # Save updated items
        save_items_file(items, session)

        return jsonify({"success": True}), 200

    except Exception as e:
        log.error(f"Error splitting item: {e}")
        return jsonify({"error": "Internal server error"}), 500


@items_page.route("/prepare_split", methods=["POST"])
def prepare_split():
    try:
        # Get current items
        items = get_current_items(session)
        if not items:
            return jsonify({"error": "No items found"}), 404

        item_count = len(items.items)
        if item_count == 0:
            return jsonify({"error": "No items to distribute"}), 400

        # Get current persons
        persons = get_current_persons(session)
        if not persons:
            return jsonify({"error": "No persons found"}), 404

        # Create array of all item indices [0, 1, 2, ...]
        all_item_indices = list(range(item_count))

        # Update each person to have all items
        for person in persons:
            person.items = all_item_indices

        # Save updated persons
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

    except Exception as e:
        log.error(f"Error preparing for split: {e}")
        return jsonify({"error": "Internal server error"}), 500
