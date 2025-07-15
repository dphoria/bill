from bill.receipts import Receipt
from bill.images import load_image
from .utils import TEST_DATA_DIR


def test_receipt_analysis_with_chat():
    image_file_path = TEST_DATA_DIR / "20241128_183627.jpg"
    image_data = load_image(image_file_path)
    receipt = Receipt(image_data)

    messages = receipt.start_analysis()

    items, messages = receipt.get_items_with_chat(messages)
    assert any(items.items)

    tax, messages = receipt.get_tax_with_chat(messages)
    assert tax.name == "Tax"
    assert 10 < tax.price < 90

    service_charge, messages = receipt.get_service_charge_with_chat(messages)
    assert service_charge.name == "Service charge"
    assert 10 < service_charge.price < 100
