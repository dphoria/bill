from bill.receipts import Items, Item
from pathlib import Path

TEST_DATA_DIR = Path(__file__).parent / ".." / "bin"


EXPECTED_ITEMS = Items(
    items=[
        Item(name="GL-Domaine Amido Cotes Du Rhone", price=13.0),
        Item(name="Bumble Bee Cooler", price=14.0),
        Item(name="Chilli Gobhi", price=12.0),
        Item(name="Makai bhel tart", price=12.0),
        Item(name="Herbed kulcha", price=6.0),
        Item(name="Cheese kulcha", price=7.0),
        Item(name="Kala tikka murg", price=23.0),
        Item(name="Kasundi jhinga", price=25.0),
        Item(name="Bengali kathi roll", price=18.0),
        Item(name="Malwani fish", price=28.0),
        Item(name="Anjeer kofta", price=24.0),
        Item(name="Tiffin box - chicken", price=62.0),
        Item(name="Amritsari lamb chops", price=38.0),
        Item(name="Mango kulfi", price=15.0),
        Item(name="Shahi tukda", price=15.0),
        Item(name="Jus d Manguir", price=9.0),
    ]
)
