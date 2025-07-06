import session_data
from flask import (
    render_template,
    session,
    Blueprint,
    request,
    jsonify,
)
from bill.receipts import Items
from logging import getLogger

log = getLogger(__file__)

distribute_page = Blueprint("distribute", __name__)


def get_current_items(session: dict) -> Items | None:
    try:
        return session_data.get_receipt_items(session)
    except Exception as e:
        log.warning(f"current list of items is empty: {e}")
        return None


def get_current_persons(session: dict) -> list | None:
    try:
        from persons import get_current_persons as get_persons

        return get_persons(session)
    except Exception as e:
        log.warning(f"current list of persons is empty: {e}")
        return None


@distribute_page.route("/distribute", methods=["GET"])
def distribute_page_view():
    # Get item index from query parameter
    item_index = request.args.get("item_index", type=int)

    # Get current items and persons
    items = get_current_items(session)
    persons = get_current_persons(session)

    # Get the specific item if index is provided
    item = None
    item_count = 0
    if items:
        item_count = len(items.items)
        if item_index is not None and 0 <= item_index < item_count:
            item = items.items[item_index]
        elif item_count > 0:
            # If no valid index provided, default to first item
            item_index = 0
            item = items.items[0]

    return render_template(
        "distribute.html",
        item=item,
        persons=persons or [],
        item_index=item_index or 0,
        item_count=item_count,
    )


@distribute_page.route("/get_item", methods=["GET"])
def get_item():
    try:
        item_index = request.args.get("item_index", type=int)

        if item_index is None:
            return jsonify({"error": "Missing item index"}), 400

        # Get current items
        items = get_current_items(session)
        if not items:
            return jsonify({"error": "No items found"}), 404

        # Validate item index
        if item_index < 0 or item_index >= len(items.items):
            return jsonify({"error": "Invalid item index"}), 400

        # Get the item
        item = items.items[item_index]

        return jsonify({"name": item.name, "price": item.price}), 200

    except Exception as e:
        log.error(f"Error getting item: {e}")
        return jsonify({"error": "Internal server error"}), 500


@distribute_page.route("/distribute_item", methods=["POST"])
def distribute_item():
    try:
        data = request.get_json()
        item_index = data.get("item_index")
        person_ids = data.get("person_ids", [])

        if item_index is None or not person_ids:
            return jsonify({"error": "Missing required fields"}), 400

        # Get current items and persons
        items = get_current_items(session)
        persons = get_current_persons(session)

        if not items:
            return jsonify({"error": "No items found"}), 404

        if not persons:
            return jsonify({"error": "No persons found"}), 404

        # Validate item index
        if item_index < 0 or item_index >= len(items.items):
            return jsonify({"error": "Invalid item index"}), 400

        # Validate person IDs
        valid_person_ids = [i for i in range(len(persons))]
        if not all(pid in valid_person_ids for pid in person_ids):
            return jsonify({"error": "Invalid person IDs"}), 400

        # Get the item to distribute
        item = items.items[item_index]
        item_price = item.price

        # Calculate distribution
        num_persons = len(person_ids)
        if num_persons == 0:
            return jsonify({"error": "No persons selected"}), 400

        # Calculate equal share
        share_per_person = item_price / num_persons

        # Create distribution result
        distribution = []
        for person_id in person_ids:
            person = persons[person_id]
            distribution.append(
                {
                    "person_id": person_id,
                    "person_name": person.name,
                    "share": share_per_person,
                }
            )

        # Calculate total distributed and remainder
        total_distributed = share_per_person * num_persons
        remainder = item_price - total_distributed

        return (
            jsonify(
                {
                    "success": True,
                    "distribution": distribution,
                    "total_distributed": total_distributed,
                    "remainder": remainder,
                    "item_name": item.name,
                    "item_price": item_price,
                    "num_persons": num_persons,
                }
            ),
            200,
        )

    except Exception as e:
        log.error(f"Error distributing item: {e}")
        return jsonify({"error": "Internal server error"}), 500


@distribute_page.route("/save_distribution", methods=["POST"])
def save_distribution():
    try:
        data = request.get_json()
        item_index = data.get("item_index")
        person_ids = data.get("person_ids", [])

        if item_index is None or not person_ids:
            return jsonify({"error": "Missing required fields"}), 400

        # Get current persons using persons.py method
        from persons import get_current_persons, save_persons_file

        persons = get_current_persons(session)
        if not persons:
            return jsonify({"error": "No persons found"}), 404

        # Validate person IDs
        valid_person_ids = [i for i in range(len(persons))]
        if not all(pid in valid_person_ids for pid in person_ids):
            return jsonify({"error": "Invalid person IDs"}), 400

        # Update each person's items list to include this item index
        for person_id in person_ids:
            person = persons[person_id]

            # Add item index to person's items if not already present
            if item_index not in person.items:
                person.items.append(item_index)

        # Save updated persons using persons.py method
        save_persons_file(persons, session)

        return jsonify({"success": True}), 200

    except Exception as e:
        log.error(f"Error saving distribution: {e}")
        return jsonify({"error": "Internal server error"}), 500
