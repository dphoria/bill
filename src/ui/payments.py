from flask import (
    render_template,
    session,
    Blueprint,
    request,
)
from bill.calculator import Calculator
from logging import getLogger
from items import get_current_items
from extras import get_current_extras
from persons import get_current_persons

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
            "share": calculator.get_person_share(item, person),
        }
        for item_index, item in enumerate(items.items)
        if item_index in person.items
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
