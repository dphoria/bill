from pydantic import BaseModel
from typing import List


class Person(BaseModel):
    name: str
    items: List[int]

    def insert_item(self, item_index: int) -> None:
        """
        Add an item to the person's items list if not already present.

        Parameters
        ----------
        item_index : int
            The index of the item to add to the person's items list.

        Returns
        -------
        None
            The items list is modified in place.
        """
        items_set = set(self.items)
        items_set.add(item_index)
        self.items = sorted(list(items_set))

    def remove_item(self, item_index: int) -> None:
        """
        Remove an item from the person's items list if present.

        Parameters
        ----------
        item_index : int
            The index of the item to remove from the person's items list.

        Returns
        -------
        None
            The items list is modified in place.
        """
        try:
            self.items.remove(item_index)
        except ValueError:
            pass

    def update_item(self, item_index: int) -> None:
        """
        Toggle an item in the person's items list - add if not present, remove if present.

        Parameters
        ----------
        item_index : int
            The index of the item to toggle in the person's items list.

        Returns
        -------
        None
            The items list is modified in place.
        """
        if item_index not in self.items:
            self.insert_item(item_index)
        else:
            self.remove_item(item_index)
