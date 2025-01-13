from bill.receipts import get_items, Items
from bill.images import load_image
from .utils import TEST_DATA_DIR, EXPECTED_ITEMS
from math import isclose
import pytest


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
