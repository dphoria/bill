from pathlib import Path
from bill.receipts import Items
from bill.person import Person
from logging import getLogger
import os
import json

log = getLogger(__file__)

DATA_DIRECTORY = "data_directory"
IMAGE_FILE = "image_file"
ITEMS_FILE = "items_file"
EXTRAS_FILE = "extras_file"
PERSONS_FILE = "persons_file"


def start_new_receipt(session: dict):
    for file in (IMAGE_FILE, ITEMS_FILE, EXTRAS_FILE, PERSONS_FILE):
        try:
            os.remove(session_item_path(session, file))
        except FileNotFoundError:
            pass

    keys_to_clear = [
        IMAGE_FILE,
        ITEMS_FILE,
        EXTRAS_FILE,
        PERSONS_FILE,
    ]

    for key in keys_to_clear:
        session.pop(key, None)


def session_item_path(session: dict, session_item_name: str) -> Path:
    return Path(session[DATA_DIRECTORY]) / session_item_name


def read_items_file(items_file_path: os.PathLike) -> Items:
    return Items.model_validate_json(json.loads(Path(items_file_path).read_text()))


def get_receipt_items(session: dict) -> Items:
    return read_items_file(session_item_path(session, ITEMS_FILE))


def save_persons_file(persons: list[Person], session: dict):
    with open(session_item_path(session, PERSONS_FILE), "w") as json_file:
        json.dump([person.model_dump() for person in persons], json_file, indent=4)


def get_current_persons(session: dict) -> list[Person]:
    try:
        persons_file = session_item_path(session, PERSONS_FILE)

        with open(persons_file, "r") as json_file:
            data = json.load(json_file)
            return [Person(**person_data) for person_data in data]

    except FileNotFoundError:
        return []
    except Exception as e:
        log.warning(f"Error reading persons file: {e}")
        return []


def save_extras_file(extras: Items, session: dict):
    with open(session_item_path(session, EXTRAS_FILE), "w") as json_file:
        json.dump(extras.model_dump_json(indent=4), json_file)


def get_current_extras(session: dict) -> Items | None:
    try:
        extras_file = session_item_path(session, EXTRAS_FILE)
        return read_items_file(extras_file)
    except Exception as e:
        log.warning(f"current list of extras is empty: {e}")
        return None
