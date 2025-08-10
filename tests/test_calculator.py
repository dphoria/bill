import pytest
from bill.calculator import Calculator
from bill.person import Person
from bill.receipts import Item, Items
from tests.utils import EXPECTED_ITEMS

SERVICE_CHARGE = "Service Charge"
TAX = "Tax"
SERVICE_CHARGE_RATIO = 0.20
TAX_RATIO = 0.1035


@pytest.fixture
def sample_persons():
    """
    Create 3 people (A, B, C) with diverse item selections for testing.

    Person A: Items 0, 2, 4, 6, 8, 10, 12, 14, 15 (wine, chilli gobhi, herbed kulcha, kala tikka murg, bengali kathi roll, anjeer kofta, amritsari lamb chops, shahi tukda, jus d manguir)
    Person B: Items 1, 3, 5, 7, 9, 11, 13, 14 (bumble bee cooler, makai bhel tart, cheese kulcha, kasundi jhinga, malwani fish, tiffin box, mango kulfi, shahi tukda)
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

    This creates different subtotals:
    - Person A: $76.50 (item 15 now shared with B)
    - Person B: $85.50 (now includes item 15 shared with A)
    - Person C: $81.00 (same as before)
    """
    person_a = Person(name="A", items=[0, 2, 4, 6, 8, 10, 12, 14, 15])
    person_b = Person(name="B", items=[1, 3, 5, 7, 9, 11, 13, 14, 15])
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
        (15, "A", 4.5, "Item shared by 2 people"),
    ],
)
def test_person_share(
    calculator, sample_persons, item_index, person_name, expected_share, description
):
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


@pytest.mark.parametrize(
    "extra_name,expected_share,description",
    [
        (SERVICE_CHARGE, 15.3, "Service charge proportional to person's subtotal"),
        (TAX, 7.91775, "Tax proportional to person's subtotal"),
    ],
)
def test_person_extra(
    calculator, sample_persons, extra_name, expected_share, description
):
    """
    Test get_person_extra method for service charge and tax.
    Uses Person A for both cases to test proportional calculation.
    """
    person_a = sample_persons[0]

    # Find the extra item by name
    extra_item = next(
        extra for extra in calculator.extras.items if extra.name == extra_name
    )

    actual_share = calculator.get_person_extra(extra_item, person_a)
    assert actual_share == pytest.approx(
        expected_share, abs=0.01
    ), f"{description}: expected {expected_share}, got {actual_share}"

    # Verify the ratio of extra share to person's subtotal matches the expected ratio
    person_subtotal = calculator.get_person_subtotal(person_a)
    actual_ratio = actual_share / person_subtotal
    expected_ratio = SERVICE_CHARGE_RATIO if extra_name == SERVICE_CHARGE else TAX_RATIO
    assert actual_ratio == pytest.approx(
        expected_ratio, abs=0.001
    ), f"{description}: ratio should be {expected_ratio}, got {actual_ratio}"


def test_person_total(calculator, sample_persons):
    """
    Test get_person_total method using Person A.
    Expected total = Person A's subtotal + service charge + tax
    """
    person_a = sample_persons[0]

    # Calculate expected total manually
    # Person A's subtotal: $76.50 (from updated calculation)
    # Service charge: $15.3 (20% of $76.50)
    # Tax: $7.91775 (10.35% of $76.50)
    expected_total = 76.50 + 15.3 + 7.91775

    actual_total = calculator.get_person_total(person_a)
    assert actual_total == pytest.approx(
        expected_total, abs=0.01
    ), f"Expected total {expected_total}, got {actual_total}"


def test_csv(calculator, sample_persons):
    csv_output = calculator.get_shares_csv()

    header = csv_output.splitlines()[0]
    expected_header = "Item,Receipt,A,B,C,Check"
    assert header == expected_header

    assert "GL-Domaine Amido Cotes Du Rhone,13.00,6.50,,6.50," in csv_output
    assert "Bumble Bee Cooler,14.00,,7.00,7.00," in csv_output
    assert "Chilli Gobhi,12.00,6.00,,6.00," in csv_output
    assert "Makai bhel tart,12.00,,6.00,6.00," in csv_output
    assert "Herbed kulcha,6.00,3.00,,3.00," in csv_output
    assert "Cheese kulcha,7.00,,3.50,3.50," in csv_output
    assert "Kala tikka murg,23.00,11.50,,11.50," in csv_output
    assert "Kasundi jhinga,25.00,,12.50,12.50," in csv_output
    assert "Bengali kathi roll,18.00,9.00,,9.00," in csv_output
    assert "Malwani fish,28.00,,14.00,14.00," in csv_output
    assert "Anjeer kofta,24.00,12.00,,12.00," in csv_output
    assert "Tiffin box - chicken,62.00,,31.00,31.00," in csv_output
    assert "Amritsari lamb chops,38.00,19.00,,19.00," in csv_output
    assert "Mango kulfi,15.00,,7.50,7.50," in csv_output
    assert "Shahi tukda,15.00,5.00,5.00,5.00," in csv_output
    assert "Jus d Manguir,9.00,4.50,4.50,," in csv_output

    subtotal = EXPECTED_ITEMS.get_sum()
    expected_subtotal_line = (
        f"Subtotal,{subtotal:.2f},76.50,91.00,153.50,{subtotal:.2f}"
    )
    assert (
        expected_subtotal_line in csv_output
    ), f"Expected '{expected_subtotal_line}' in CSV output"

    service_charge = subtotal * SERVICE_CHARGE_RATIO
    assert (
        f"Service Charge,{service_charge:.2f},15.30,18.20,30.70,{service_charge:.2f}"
        in csv_output
    )

    tax = subtotal * TAX_RATIO
    assert f"Tax,{tax:.2f},7.92,9.42,15.89,{tax:.2f}" in csv_output

    total = subtotal + service_charge + tax
    assert f"Total,{total:.2f},99.72,118.62,200.09,{total:.2f}" in csv_output


def test_person_update_item():
    """
    Test Person.update_item() method to ensure it correctly toggles items.
    Tests both insert_item() and remove_item() scenarios.
    """
    person = Person(name="Test", items=[1, 3, 5])

    person.update_item(7)
    assert person.items == [
        1,
        3,
        5,
        7,
    ], "Item 7 should be added and list should be sorted"

    person.update_item(3)
    assert person.items == [1, 3, 5, 7], "Item 3 should remain unchanged"

    person.update_item(5)
    assert person.items == [1, 3, 7], "Item 5 should be removed"

    person.update_item(9)
    assert person.items == [1, 3, 7], "Item 9 should not affect the list"

    person.update_item(5)
    assert person.items == [1, 3, 5, 7], "Item 5 should be added back"

    person.update_item(5)
    assert person.items == [1, 3, 7], "Item 5 should be removed again"
