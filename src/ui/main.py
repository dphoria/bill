from flask import render_template, request, flash, url_for, redirect, session
from app import app
from bill.images import load_image
import session_data
from tempfile import TemporaryDirectory


_data_directory = None


@app.route("/", methods=["GET"])
def home():
    session[session_data.DATA_DIRECTORY] = _data_directory
    return render_template("index.html")


def save_image(image_file, session):
    image_file_path = session_data.session_item_path(session, session_data.IMAGE_FILE)
    image_file_path.write_bytes(load_image(image_file))


@app.route("/", methods=["POST"])
def read_receipt_image():
    session_data.start_new_receipt()

    try:
        image_file = request.files["file"]
        save_image(image_file, session)
        return redirect(url_for("items.list_items"))
    except KeyError:
        flash("No file uploaded")
    except Exception as e:
        flash(str(e))

    return redirect(url_for("home"))


if __name__ == "__main__":
    with TemporaryDirectory() as dir:
        _data_directory = str(dir)
        app.run(host="0.0.0.0", port=8000)
