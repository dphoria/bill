import pytest
from bill.person import Person
from bill.receipts import Items
from tests.utils import EXPECTED_ITEMS

SERVICE_CHARGE = "Service Charge"
TAX = "Tax"


@pytest.fixture
def sample_persons():
    """
    Create 3 people (A, B, C) with diverse item selections for testing.

    Person A: Items 0, 2, 4, 6, 8, 10, 12, 14, 15 (wine, chilli gobhi, herbed kulcha, kala tikka murg, bengali kathi roll, anjeer kofta, amritsari lamb chops, mango kulfi, jus d manguir)
    Person B: Items 1, 3, 5, 7, 9, 11, 13, 15 (bumble bee cooler, makai bhel tart, cheese kulcha, kasundi jhinga, malwani fish, tiffin box, shahi tukda, jus d manguir)
    Person C: Items 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 (all items except item 15)

    This creates scenarios where:
    - Item 0 (GL-Domaine Amido Cotes Du Rhone) is shared by Person A and Person C
    - Item 1 (Bumble Bee Cooler) is shared by Person B and Person C
    - Item 2 (Chilli Gobhi) is shared by Person A and Person C
    - Item 3 (Makai bhel tart) is shared by Person B and Person C
    - Item 4 (Herbed kulcha) is shared by Person A and Person C
    - Item 5 (Cheese kulcha) is shared by Person B and Person C
    - Item 6 (Kala tikka murg) is shared by Person A and Person C
    - Item 7 (Kasundi jhinga) is shared by Person B and Person C
    - Item 8 (Bengali kathi roll) is shared by Person A and Person C
    - Item 9 (Malwani fish) is shared by Person B and Person C
    - Item 10 (Anjeer kofta) is shared by Person A and Person C
    - Item 11 (Tiffin box - chicken) is shared by Person B and Person C
    - Item 12 (Amritsari lamb chops) is shared by Person A and Person C
    - Item 13 (Mango kulfi) is shared by Person B and Person C
    - Item 14 (Shahi tukda) is shared by ALL THREE people (A, B, C)
    - Item 15 (Jus d Manguir) is paid entirely by Person A only
    """
    person_a = Person(name="A", items=[0, 2, 4, 6, 8, 10, 12, 14, 15])
    person_b = Person(name="B", items=[1, 3, 5, 7, 9, 11, 13, 14])
    person_c = Person(
        name="C", items=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    )

    return [person_a, person_b, person_c]


@pytest.fixture
def calculator(sample_persons):
    """
    Create a Calculator object with the sample persons, items from utils, and extra items for service charge and tax.

    Extra items:
    - Service charge: 20% of subtotal
    - Tax: 10.35% of subtotal
    """
    from bill.calculator import Calculator
    from bill.receipts import Item

    # Calculate subtotal from EXPECTED_ITEMS
    subtotal = EXPECTED_ITEMS.get_sum()

    # Create extra items
    service_charge = Item(name=SERVICE_CHARGE, price=subtotal * 0.20)
    tax = Item(name=TAX, price=subtotal * 0.1035)
    extras = Items(items=[service_charge, tax])

    return Calculator(persons=sample_persons, items=EXPECTED_ITEMS, extras=extras)


@pytest.mark.parametrize(
    "item_index,person_name,expected_share,description",
    [
        (14, "A", 5.0, "Item shared by all 3 people"),
        (0, "A", 6.5, "Item shared by 2 people"),
        (0, "B", 0.0, "Person doesn't have the item"),
        (15, "A", 9.0, "Item paid entirely by one person"),
    ],
)
def test_person_share(
    calculator, sample_persons, item_index, person_name, expected_share, description
):
    """
    Test get_person_share method with various scenarios:
    - Item shared by all 3 people
    - Item shared by 2 people
    - Person not having the item
    """
    person_map = {
        "A": sample_persons[0],
        "B": sample_persons[1],
        "C": sample_persons[2],
    }
    item = EXPECTED_ITEMS.items[item_index]
    person = person_map[person_name]

    actual_share = calculator.get_person_share(item, person)
    assert (
        actual_share == expected_share
    ), f"{description}: expected {expected_share}, got {actual_share}"
