from copy import deepcopy
import pytest
from .utils import EXPECTED_ITEMS


@pytest.mark.parametrize(
    "name,split_item_price",
    [("Bumble Bee Cooler", None), ("Tiffin box - chicken", 31.0)],
)
def test_item_split(name: str, split_item_price: float | None):
    items = deepcopy(EXPECTED_ITEMS.items)
    items[11].count = 3
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


@pytest.mark.parametrize("index,split_item_price", [(0, None), (11, 31.0)])
def test_items_split(index: int, split_item_price: float | None):
    items = deepcopy(EXPECTED_ITEMS)
    next_item = items.items[index + 1]
    items.split(index)
    assert split_item_price is None or items.items[index + 1].price == split_item_price

    next_item_index = index + 1 if split_item_price is None else index + 2
    assert items.items[next_item_index] == next_item
