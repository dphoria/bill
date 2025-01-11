from flask import render_template, request, flash, url_for, redirect, session
from app import app
from bill.images import load_image
from base64 import urlsafe_b64encode
from constants import RECEIPT_IMAGE_DATA


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def read_receipt_image():
    try:
        image_file = request.files["file"]
        image_data = load_image(image_file)
        session[RECEIPT_IMAGE_DATA] = urlsafe_b64encode(image_data).decode()
        # flash(f"{image_file.filename}: {len(image_data)}")
        return redirect(url_for("list_items"))
    except KeyError:
        flash("No file uploaded")
    except Exception as e:
        flash(str(e))
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
