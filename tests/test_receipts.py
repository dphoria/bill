from bill.receipts import get_items, Item, Items
from bill.images import load_image
from .utils import TEST_DATA_DIR
from math import isclose
import pytest

EXPECTED_ITEMS = Items(
    items=[
        Item(name="GL-Domaine Amido Cotes Du Rhone", count=1, price=13.0),
        Item(name="Bumble Bee Cooler", count=1, price=14.0),
        Item(name="Chilli Gobhi", count=1, price=12.0),
        Item(name="Makai bhel tart", count=1, price=12.0),
        Item(name="Herbed kulcha", count=1, price=6.0),
        Item(name="Cheese kulcha", count=1, price=7.0),
        Item(name="Kala tikka murg", count=1, price=23.0),
        Item(name="Kasundi jhinga", count=1, price=25.0),
        Item(name="Bengali kathi roll", count=1, price=18.0),
        Item(name="Malwani fish", count=1, price=28.0),
        Item(name="Anjeer kofta", count=1, price=24.0),
        Item(name="Tiffin box - chicken", count=2, price=62.0),
        Item(name="Amritsari lamb chops", count=1, price=38.0),
        Item(name="Mango kulfi", count=1, price=15.0),
        Item(name="Shahi tukda", count=1, price=15.0),
        Item(name="Jus d Manguir", count=1, price=9.0),
    ]
)


@pytest.fixture(scope="session")
def receipt_items() -> Items:
    image_file_path = TEST_DATA_DIR / "20241128_183627.jpg"
    image_data = load_image(image_file_path)
    items = get_items(image_data)
    return items


def test_item_counts(receipt_items):
    assert any(receipt_items.items)


def test_subtotal(receipt_items):
    assert isclose(EXPECTED_ITEMS.get_sum(), 321.0, abs_tol=0.01)
