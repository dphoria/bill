from bill.person import Person
from bill.receipts import Items, Item


class Calculator:
    """
    A calculator for splitting bills among persons based on items and extras.
    """

    def __init__(self, persons: list[Person], items: Items, extras: Items):
        """
        Initialize the calculator with persons, items, and extras.

        Parameters
        ----------
        persons: list[Person]
            List of Person objects representing the people splitting the bill
        items: Items
            Items object containing the main items to be split
        extras: Items
            Items object containing additional items (tax, tip, etc.) to be split
        """
        self.persons = persons
        self.items = items
        self.extras = extras

    def get_split_count(self, item: Item) -> int:
        """
        Get the number of persons who have this item in their items list.

        Parameters
        ----------
        item: Item
            The item to count splits for

        Returns
        -------
        int
            The number of persons who have this item
        """
        item_index = self.items.items.index(item)
        return sum(1 for person in self.persons if item_index in person.items)

    def get_person_share(self, item: Item, person: Person) -> float:
        """
        Calculate the share of a specific item for a specific person.

        Parameters
        ----------
        item: Item
            The item to calculate the share for
        person: Person
            The person to calculate the share for

        Returns
        -------
        float
            The person's share of the item price (0.0 if person doesn't have this item)
        """
        item_index = self.items.items.index(item)

        if item_index in person.items:
            split_count = self.get_split_count(item)
            return item.price / split_count
        else:
            return 0.0

    def get_person_subtotal(self, person: Person) -> float:
        """
        Calculate the subtotal for a specific person based on their items.

        Parameters
        ----------
        person: Person
            The person to calculate the subtotal for

        Returns
        -------
        float
            The person's subtotal (sum of their shares of all items)
        """
        shares = map(lambda item: self.get_person_share(item, person), self.items.items)
        return sum(shares)

    def get_person_extra(self, extra: Item, person: Person) -> float:
        """
        Calculate a person's share of an extra item (tax, tip, etc.) based on their proportional share of the bill.

        Parameters
        ----------
        extra: Item
            The extra item to calculate the share for (tax, tip, etc.)
        person: Person
            The person to calculate the share for

        Returns
        -------
        float
            The person's share of the extra item based on their proportional share of the bill
        """
        receipt_subtotal = self.items.get_sum()
        person_ratio = self.get_person_subtotal(person) / receipt_subtotal
        return extra.price * person_ratio

    def get_person_total(self, person: Person) -> float:
        """
        Calculate the total amount a person owes including items and extras.

        Parameters
        ----------
        person: Person
            The person to calculate the total for

        Returns
        -------
        float
            The person's total amount (subtotal + all extras)
        """
        person_subtotal = self.get_person_subtotal(person)
        person_extras = map(
            lambda extra: self.get_person_extra(extra, person), self.extras.items
        )
        return person_subtotal + sum(person_extras)
