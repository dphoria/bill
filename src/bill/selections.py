from pydantic import BaseModel
from bill.receipts import Item, Items


class ItemSelection(BaseModel):
    item: Item
    selected: bool


def get_item_selections(items: Items, selected_items: list[int]) -> list[ItemSelection]:
    def create_selection(index_item):
        index, item = index_item
        is_selected = index in selected_items
        return ItemSelection(item=item, selected=is_selected)

    item_selections = map(create_selection, enumerate(items.items))
    return list(item_selections)
