from bill.receipts import parse_item
import pytest

# @pytest.fixture(scope="session")
# def receipt_description() -> list[str]:
#     image_file_path = TEST_DATA_DIR / "20241128_183627.jpg"
#     image_data = load_image(image_file_path)
#     description = read_receipt(image_data)
#     description = list(description)
#     return description

# def test_receipt_description(receipt_description):
#     num_expected_items = 16
#     assert len(receipt_description) >= num_expected_items

@pytest.fixture()
def sample_receipt_description() -> list[str]:
    return """- GL-Domaine Amido Cotes Du Rhone, 1, $13.00
- Bumble Bee Cooler, 1, $14.00
- Chilli Gobhi, 1, $12.00
- Makai Bhel Tart, 1, $12.00
- Herbed Kulcha, 1, $6.00
- Cheese Kulcha, 1, $7.00
- Kala Tikka Murg, 1, $23.00
- Kasundi Jhinga, 1, $25.00
- Bengali Kati Roll, 1, $18.00
- Malwani Fish, 1, $28.00
- Anjeer Kofta, 1, $24.00
- Tiffin Box - Chicken, 2, $62.00
- Amritsari Lamb Chops, 1, $38.00
- Mango Kulfi, 1, $15.00
- Shahi Tukda, 1, $15.00
- Jus d Manguir, 1, $9.00

Note: I use the a.m.d subscript for the list item number if there are more than one item of the same food name. In our list it happens in the food called Tiffin Box - Chicken, where we are selling 2 items instead of just 1.""".splitlines()

def test_parse_item(sample_receipt_description):
    assert parse_item(sample_receipt_description[0])
    assert not parse_item(sample_receipt_description[-1])
