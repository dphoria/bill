from bill.receipts import Items, Item
from pathlib import Path

TEST_DATA_DIR = Path(__file__).parent / ".." / "bin"


EXPECTED_ITEMS = Items(
    items=[
        Item(name="GL-Domaine Amido Cotes Du Rhone", count=1, price=13.0),
        Item(name="Bumble Bee Cooler", count=1, price=14.0),
        Item(name="Chilli Gobhi", count=1, price=12.0),
        Item(name="Makai bhel tart", count=1, price=12.0),
        Item(name="Herbed kulcha", count=1, price=6.0),
        Item(name="Cheese kulcha", count=1, price=7.0),
        Item(name="Kala tikka murg", count=1, price=23.0),
        Item(name="Kasundi jhinga", count=1, price=25.0),
        Item(name="Bengali kathi roll", count=1, price=18.0),
        Item(name="Malwani fish", count=1, price=28.0),
        Item(name="Anjeer kofta", count=1, price=24.0),
        Item(name="Tiffin box - chicken", count=2, price=62.0),
        Item(name="Amritsari lamb chops", count=1, price=38.0),
        Item(name="Mango kulfi", count=1, price=15.0),
        Item(name="Shahi tukda", count=1, price=15.0),
        Item(name="Jus d Manguir", count=1, price=9.0),
    ]
)
