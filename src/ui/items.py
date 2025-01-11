from flask import render_template, session
from app import app
from bill.receipts import get_items
from constants import RECEIPT_IMAGE_DATA
from base64 import urlsafe_b64decode


@app.route("/items")
def list_items():
    image_data = session[RECEIPT_IMAGE_DATA]
    image_data = urlsafe_b64decode(image_data)
    items = get_items(image_data)
    return render_template("items.html", items=items)
