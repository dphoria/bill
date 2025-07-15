import session_data
from flask import (
    render_template,
    session,
    Blueprint,
    request,
    jsonify,
)
from bill.receipts import Items, Item, Receipt
from pathlib import Path
from logging import getLogger
from items import get_current_items

log = getLogger(__file__)

extras_page = Blueprint("extras", __name__)


def get_receipt_extras(session: dict) -> Items:
    try:
        image_file_path = session_data.session_item_path(
            session, session_data.IMAGE_FILE
        )
        image_data = Path(image_file_path).read_bytes()
        receipt = Receipt(image_data)

        chat_messages = list(session_data.get_chat_messages(session))
        service_charge, chat_messages = receipt.get_service_charge_with_chat(
            chat_messages
        )
        tax, chat_messages = receipt.get_tax_with_chat(chat_messages)

        session_data.save_chat_messages(chat_messages, session)

        return Items(items=[service_charge, tax])
    except Exception as e:
        log.warning(f"Error extracting service charge and tax from receipt image: {e}")
        return None


def get_default_extras() -> Items:
    default_extras = [
        Item(name="Service charge", price=0.0),
        Item(name="Tax", price=0.0),
    ]
    return Items(items=default_extras)


def get_current_extras(session: dict) -> Items:
    extras = session_data.get_current_extras(session)
    extras = extras or get_receipt_extras(session)
    extras = extras or get_default_extras()
    return extras


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
