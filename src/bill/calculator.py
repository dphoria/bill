import csv
from io import StringIO, BytesIO
from typing import Iterable
from bill.person import Person
from bill.receipts import Items, Item
from openpyxl import Workbook


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

    def get_person_shares(self, person: Person) -> "Iterable[tuple[Item, float]]":
        """
        Lazily compute a person's shares across all items, paired with items.

        Parameters
        ----------
        person: Person
            The person to calculate shares for

        Returns
        -------
        Iterable[tuple[Item, float]]
            A lazy iterable yielding (Item, share) tuples for each item in self.items.items.
        """
        return map(
            lambda item: (item, self.get_person_share(item, person)), self.items.items
        )

    def get_shares_csv(self):
        """
        Get a CSV string of shares for each person.
        """

        def get_person_shares(get_share):
            return [get_share(person) for person in self.persons]

        fieldnames = (
            ["Item", "Receipt"] + [person.name for person in self.persons] + ["Check"]
        )

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for item in self.items.items:
            row = {"Item": item.name, "Receipt": f"{item.price:.2f}"}
            for person in self.persons:
                share = self.get_person_share(item, person)
                row[person.name] = f"{share:.2f}" if share else ""
            row["Check"] = ""
            writer.writerow(row)

        subtotal = self.items.get_sum()
        person_subtotals = get_person_shares(self.get_person_subtotal)
        subtotal_row = {"Item": "Subtotal", "Receipt": f"{subtotal:.2f}"}
        for person, share in zip(self.persons, person_subtotals):
            subtotal_row[person.name] = f"{share:.2f}"
        subtotal_row["Check"] = f"{sum(person_subtotals):.2f}"
        writer.writerow(subtotal_row)

        for extra in self.extras.items:
            extra_shares = get_person_shares(
                lambda person: self.get_person_extra(extra, person)
            )
            extra_row = {"Item": extra.name, "Receipt": f"{extra.price:.2f}"}
            for person, share in zip(self.persons, extra_shares):
                extra_row[person.name] = f"{share:.2f}" if share else ""
            extra_row["Check"] = f"{sum(extra_shares):.2f}"
            writer.writerow(extra_row)

        total = subtotal + sum(extra.price for extra in self.extras.items)
        person_totals = get_person_shares(self.get_person_total)
        total_row = {"Item": "Total", "Receipt": f"{total:.2f}"}
        for person, share in zip(self.persons, person_totals):
            total_row[person.name] = f"{share:.2f}"
        total_row["Check"] = f"{sum(person_totals):.2f}"
        writer.writerow(total_row)

        output.seek(0)
        return output.getvalue()

    def get_shares_spreadsheet(self):
        """
        Get an Excel spreadsheet (BytesIO) with formulas for calculating shares.
        """
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Bill Split"

        fieldnames = (
            ["Item", "Receipt"] + [person.name for person in self.persons] + ["Check"]
        )

        worksheet.append(fieldnames)
        current_row = 2

        for item in self.items.items:
            row_data = [item.name, item.price]
            split_count = self.get_split_count(item)
            item_index = self.items.items.index(item)

            for person in self.persons:
                if item_index in person.items:
                    formula = f"=$B{current_row}/{split_count}"
                    row_data.append(formula)
                else:
                    row_data.append(None)
            row_data.append(None)
            worksheet.append(row_data)
            current_row += 1

        subtotal_row = current_row
        subtotal = self.items.get_sum()
        person_count = len(self.persons)
        last_person_col = chr(ord("C") + person_count - 1)

        row_data = ["Subtotal", subtotal]
        for col_idx in range(person_count):
            col_letter = chr(ord("C") + col_idx)
            formula = f"=SUM({col_letter}2:{col_letter}{current_row - 1})"
            row_data.append(formula)
        row_data.append(f"=SUM(C{current_row}:{last_person_col}{current_row})")
        worksheet.append(row_data)
        current_row += 1

        for extra in self.extras.items:
            percentage = (extra.price / subtotal) * 100
            if percentage == int(percentage):
                formatted_percentage = f"{int(percentage)}%"
            else:
                formatted_percentage = f"{percentage:.2f}%"
            extra_name_with_percentage = f"{extra.name} ({formatted_percentage})"

            row_data = [extra_name_with_percentage, extra.price]
            for col_idx in range(person_count):
                col_letter = chr(ord("C") + col_idx)
                formula = (
                    f"=({col_letter}{subtotal_row}/$B${subtotal_row})*$B{current_row}"
                )
                row_data.append(formula)
            row_data.append(f"=SUM(C{current_row}:{last_person_col}{current_row})")
            worksheet.append(row_data)
            current_row += 1

        total_row = current_row
        row_data = ["Total"]
        row_data.append(f"=SUM(B{subtotal_row}:B{current_row - 1})")
        for col_idx in range(person_count):
            col_letter = chr(ord("C") + col_idx)
            formula = f"=SUM({col_letter}{subtotal_row}:{col_letter}{current_row - 1})"
            row_data.append(formula)
        row_data.append(f"=SUM(C{total_row}:{last_person_col}{total_row})")
        worksheet.append(row_data)

        output = BytesIO()
        workbook.save(output)
        output.seek(0)
        return output
