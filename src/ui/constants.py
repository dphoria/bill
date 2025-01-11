from pathlib import Path


DATA_DIRECTORY = "data_directory"
IMAGE_FILE = "image_file"
ITEMS_FILE = "items_file"
PEOPLE = "people"


def session_item_path(session: dict, session_item_name: str) -> Path:
    return Path(session[DATA_DIRECTORY]) / session_item_name


def get_people(session: dict) -> list[str]:
    people = session.get(PEOPLE, "").split(",")
    return people


def save_people(session: dict, people: list[str]):
    session[PEOPLE] = ",".join(sorted(set(people), key=str.lower))
