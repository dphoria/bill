from flask import render_template, session, Blueprint
from bill.receipts import get_items
from constants import Session
from pathlib import Path

items_page = Blueprint("items", __name__)


@items_page.route("/items")
def list_items():
    image_file_path = session[Session.image_file_path]
    image_data = Path(image_file_path).read_bytes()
    items = get_items(image_data)
    return render_template("items.html", items=items.items)
