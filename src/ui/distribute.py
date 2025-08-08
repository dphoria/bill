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
    person_index = request.args.get("person_index", type=int) or 0

    items = get_current_items(session)
    persons = get_current_persons(session)
    person = persons[person_index] if persons and 0 <= person_index < len(persons) else None

    # Calculate per-item share for this person using map and list comprehension
    def share_for_item(args):
        idx, item = args
        count = sum(1 for p in persons if idx in p.items)
        share = item.price / count if person and idx in person.items and count > 0 else 0.0
        return {
            "name": item.name,
            "price": item.price,
            "share": share,
        }
    item_shares = list(map(share_for_item, enumerate(items.items)))

    return render_template(
        "distribute.html",
        items=item_shares,
        person=person,
        person_index=person_index,
        person_count=len(persons),
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

    return (
        jsonify(
            {
                "success": True,
                "distribution": distribution,
                "total_distributed": total_distributed,
                "item_name": item.name,
                "item_price": item.price,
                "num_persons": num_persons,
            }
        ),
        200,
    )


@distribute_page.route("/get_persons", methods=["GET"])
def get_persons_api():
    persons = get_current_persons(session)
    return jsonify([p.model_dump() for p in persons]), 200

@distribute_page.route("/get_items", methods=["GET"])
def get_items_api():
    items = get_current_items(session)
    return jsonify([{"name": i.name, "price": i.price} for i in items.items]), 200

@distribute_page.route("/save_distribution", methods=["POST"])
def save_distribution():
    data = request.get_json()
    person_index = data.get("person_index")
    item_index = data.get("item_index")
    add = data.get("add", True)

    persons = get_current_persons(session)
    if 0 <= person_index < len(persons):
        person = persons[person_index]
        if add:
            if item_index not in person.items:
                person.items.append(item_index)
                person.items.sort()
        else:
            if item_index in person.items:
                person.items.remove(item_index)
        save_persons_file(persons, session)
    return jsonify({"success": True}), 200
