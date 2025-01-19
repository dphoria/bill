from flask import render_template, Blueprint, session, request, redirect, url_for
from logging import getLogger
import session_data

log = getLogger(__file__)

extras_page = Blueprint("extras", __name__)


@extras_page.route("/extras", methods=["GET"])
def home():
    return render_template("extras.html")


@extras_page.route("/extras", methods=["POST"])
def save_extras():
    session[session_data.TAX_PERCENT] = float(request.form["tax-percent"])
    session[session_data.TIP_PERCENT] = float(request.form["tip-percent"])
    return redirect(url_for("selections.home"))
