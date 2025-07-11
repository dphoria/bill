from flask import (
    render_template,
    session,
    Blueprint,
    request,
    jsonify,
)
from logging import getLogger
from items import get_current_items
from persons import get_current_persons, save_persons_file

log = getLogger(__file__)

distribute_page = Blueprint("distribute", __name__)


@distribute_page.route("/distribute", methods=["GET"])
def distribute_page_view():
    item_index = request.args.get("item_index", type=int) or 0

    items = get_current_items(session)
    persons = get_current_persons(session)
    item = items.items[item_index]

    return render_template(
        "distribute.html",
        item=item,
        persons=persons or [],
        item_index=item_index or 0,
        item_count=len(items.items),
    )


@distribute_page.route("/get_item", methods=["GET"])
def get_item():
    item_index = request.args.get("item_index", type=int) or 0

    items = get_current_items(session)
    item = items.items[item_index]

    return jsonify({"name": item.name, "price": item.price}), 200


@distribute_page.route("/distribute_item", methods=["POST"])
def distribute_item():
    data = request.get_json()
    item_index = data.get("item_index")
    person_ids = data.get("person_ids", [])

    items = get_current_items(session)
    persons = get_current_persons(session)
    item = items.items[item_index]

    num_persons = len(person_ids)
    share_per_person = item.price / num_persons

    distribution = [
        {
            "person_id": person_id,
            "person_name": persons[person_id].name,
            "share": share_per_person,
        }
        for person_id in person_ids
    ]

    total_distributed = share_per_person * num_persons
    remainder = item.price - total_distributed

    return (
        jsonify(
            {
                "success": True,
                "distribution": distribution,
                "total_distributed": total_distributed,
                "remainder": remainder,
                "item_name": item.name,
                "item_price": item.price,
                "num_persons": num_persons,
            }
        ),
        200,
    )


@distribute_page.route("/save_distribution", methods=["POST"])
def save_distribution():
    data = request.get_json()
    item_index = data.get("item_index")
    person_ids = data.get("person_ids", [])

    persons = get_current_persons(session)

    for person_id, person in enumerate(persons):
        if person_id in person_ids:
            person.items = sorted(set(person.items + [item_index]))
        elif item_index in person.items:
            person.items.remove(item_index)

    save_persons_file(persons, session)

    return jsonify({"success": True}), 200
