import pytest
from .utils import EXPECTED_ITEMS
from bill.selections import get_item_selections, ItemSelection


@pytest.mark.parametrize(
    "selected_items,expected_selections",
    [([], []), ([-1], []), ([100], []), ([3, 5], [3, 5])],
)
def test_selections(selected_items, expected_selections):
    selections = get_item_selections(EXPECTED_ITEMS, selected_items)
    selections = list(filter(lambda selection: selection.selected, selections))

    assert len(selections) == len(expected_selections)
    for item_index in expected_selections:
        item = ItemSelection(item=EXPECTED_ITEMS.items[item_index], selected=True)
        assert item in selections
