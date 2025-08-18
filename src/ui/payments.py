from flask import (
    render_template,
    session,
    Blueprint,
    request,
    Response,
    jsonify,
)
from bill.calculator import Calculator
from logging import getLogger
from items import get_current_items
from extras import get_current_extras
from persons import get_current_persons
from session_data import save_persons_file
from datetime import datetime

log = getLogger(__file__)

payments_page = Blueprint("payments", __name__)


@payments_page.route("/payments", methods=["GET"])
def payments_page_view():
    items = get_current_items(session)
    extras = get_current_extras(session)
    persons = get_current_persons(session)

    person_index = request.args.get("person_index", type=int) or 0
    person = persons[person_index]

    calculator = Calculator(persons=persons, items=items, extras=extras)

    items_total = items.get_sum()
    extras_total = extras.get_sum()
    overall_total = items_total + extras_total

    person_items = [
        {
            "name": item.name,
            "price": item.price,
            "share": share,
        }
        for item, share in calculator.get_person_shares(person)
    ]

    person_extras = [
        {
            "name": extra.name,
            "price": extra.price,
            "share": calculator.get_person_extra(extra, person),
        }
        for extra in extras.items
    ]

    person_subtotal = calculator.get_person_subtotal(person)
    person_total = calculator.get_person_total(person)

    return render_template(
        "payments.html",
        person=person,
        persons=persons,
        person_index=person_index,
        person_count=len(persons),
        person_items=person_items,
        person_extras=person_extras,
        person_subtotal=person_subtotal,
        person_total=person_total,
        items_total=items_total,
        extras_total=extras_total,
        overall_total=overall_total,
    )


@payments_page.route("/payments/download", methods=["GET"])
def download_csv():
    items = get_current_items(session)
    extras = get_current_extras(session)
    persons = get_current_persons(session)

    calculator = Calculator(persons=persons, items=items, extras=extras)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}.csv"

    csv_content = calculator.get_shares_csv()

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@payments_page.route("/share_item", methods=["POST"])
def share_item():
    data = request.get_json()
    item_index = data.get("item_index")
    person_index = data.get("person_index")

    persons = get_current_persons(session)
    person = persons[person_index]
    person.update_item(item_index)
    save_persons_file(persons, session)

    items = get_current_items(session)
    extras = get_current_extras(session)
    calculator = Calculator(persons=persons, items=items, extras=extras)
    item = items.items[item_index]
    share = calculator.get_person_share(item, person)

    person_subtotal = calculator.get_person_subtotal(person)
    person_total = calculator.get_person_total(person)

    return (
        jsonify(
            {
                "success": True,
                "share": share,
                "item_name": item.name,
                "item_price": item.price,
                "person_subtotal": person_subtotal,
                "person_total": person_total,
            }
        ),
        200,
    )
