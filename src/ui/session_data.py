from pathlib import Path
from bill.receipts import Items
from bill.selections import ItemSelection, get_item_selections
import os
import json


DATA_DIRECTORY = "data_directory"
IMAGE_FILE = "image_file"
ITEMS_FILE = "items_file"
SELECTIONS_FILE = "selections_file"
PEOPLE = "people"
CURRENT_PERSON = "current_person"


def session_item_path(session: dict, session_item_name: str) -> Path:
    return Path(session[DATA_DIRECTORY]) / session_item_name


def read_items_file(items_file_path: os.PathLike) -> Items:
    return Items.model_validate_json(json.loads(Path(items_file_path).read_text()))


def get_receipt_items(session: dict) -> Items:
    return read_items_file(session_item_path(session, ITEMS_FILE))


def get_people(session: dict) -> list[str]:
    people = session.get(PEOPLE, "").strip()
    return people.split(",") if people else []


def save_people(session: dict, people: list[str]):
    people = [name.strip() for name in people]
    session[PEOPLE] = ",".join(sorted(set(people), key=str.lower))


def get_person_selections(session: dict, person: str | None) -> list[ItemSelection]:
    items = get_receipt_items(session)

    try:
        selections = json.loads(session_item_path(session, SELECTIONS_FILE).read_text())
    except FileNotFoundError:
        selections = {}

    person_selections = selections.get(person, []) if person else []
    person_selected_items = get_item_selections(items, person_selections)
    return person_selected_items
