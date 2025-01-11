from flask import Flask, render_template, request, flash, url_for, redirect
import os

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def read_receipt_image():
    try:
        image_file = request.files["file"]
        image_data = image_file.read()
        flash(f"{image_file.filename}: {len(image_data)}")
    except KeyError:
        flash("No file uploaded")
    except Exception as e:
        flash(str(e))
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
