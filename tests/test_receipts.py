import math
from bill.receipts import get_items, Item
from bill.images import load_image, get_image_data, compress
from .utils import TEST_DATA_DIR
import pytest

@pytest.fixture(scope="session")
def receipt_items() -> list[Item]:
    image_file_path = TEST_DATA_DIR / "20241128_183627.jpg"
    image_data = load_image(image_file_path)
    items = list(get_items(image_data))

    for item in items:
        print(item)

    return items

def test_item_counts(receipt_items):
    assert len(receipt_items) == 16
    assert receipt_items[11].count == 2

def test_subtotal(receipt_items):
    prices = [item.price for item in receipt_items]
    subtotal = sum(prices)
    assert math.isclose(subtotal, 321, abs_tol=0.01)
