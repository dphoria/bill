from bill.receipts import Receipt, Items
from bill.images import load_image
from .utils import TEST_DATA_DIR, EXPECTED_ITEMS
from math import isclose
import pytest


@pytest.fixture(scope="session")
def receipt_container() -> Receipt:
    image_file_path = TEST_DATA_DIR / "20241128_183627.jpg"
    image_data = load_image(image_file_path)
    receipt = Receipt(image_data)
    return receipt


@pytest.fixture(scope="session")
def receipt_items(receipt_container) -> Items:
    items = receipt_container.get_items()
    return items


def test_items_exist(receipt_items):
    assert any(receipt_items.items)


def test_items_sum(receipt_items):
    assert isclose(EXPECTED_ITEMS.get_sum(), 321.0, abs_tol=0.01)


def test_subtotal(receipt_container):
    subtotal = receipt_container.get_subtotal()
    assert subtotal.name == "Subtotal"
    assert 250 < subtotal.price < 400


def test_tax(receipt_container):
    tax = receipt_container.get_tax()
    assert tax.name == "Tax"
    assert 10 < tax.price < 90


def test_service_charge(receipt_container):
    service_charge = receipt_container.get_service_charge()
    assert service_charge.name == "Service charge"
    assert 10 < service_charge.price < 100
