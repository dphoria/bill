from flask import render_template, request, flash, url_for, redirect, session
from app import app
from bill.images import load_image
from constants import Session
from pathlib import Path
from tempfile import TemporaryDirectory

data_directory = None
IMAGE_FILE_NAME = "RECEIPT_IMAGE"


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


def save_image(image_file) -> str:
    image_file_path = Path(data_directory) / IMAGE_FILE_NAME
    image_file_path.write_bytes(load_image(image_file))
    return str(image_file_path)


@app.route("/", methods=["POST"])
def read_receipt_image():
    try:
        image_file = request.files["file"]
        image_file_path = save_image(image_file)
        session[Session.image_file_path] = image_file_path
        return redirect(url_for("items.list_items"))
    except KeyError:
        flash("No file uploaded")
    except Exception as e:
        flash(str(e))
    return redirect(url_for("home"))


if __name__ == "__main__":
    with TemporaryDirectory() as dir:
        data_directory = dir
        app.run(host="0.0.0.0", port=8000)
