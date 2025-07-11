from copy import deepcopy
import pytest
from .utils import EXPECTED_ITEMS


@pytest.mark.parametrize(
    "name,split_item_price",
    [("Bumble Bee Cooler", 7.0), ("Tiffin box - chicken", 46.5)],
)
def test_item_split(name: str, split_item_price: float | None):
    items = deepcopy(EXPECTED_ITEMS.items)
    items[11].price = 93.0

    for item in items:
        if item.name == name:
            split_items = item.split()
            try:
                assert split_items[1].price == split_item_price
                assert split_items[0].price == item.price - split_item_price
            except IndexError:
                assert split_item_price is None
            break
    else:
        assert False


@pytest.mark.parametrize("index,split_item_price", [(0, 6.5), (11, 46.5)])
def test_items_split(index: int, split_item_price: float | None):
    items = deepcopy(EXPECTED_ITEMS)
    original_item = items.items[index]
    items.split(index)
    new_items = items.items[index : index + 2]
    prices = sorted([item.price for item in new_items])
    expected_prices = sorted([split_item_price, original_item.price - split_item_price])
    assert prices == expected_prices
