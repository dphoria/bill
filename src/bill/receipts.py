import os
import base64
from openai import OpenAI
from pydantic import BaseModel
from logging import getLogger

log = getLogger(__file__)

INFERENCE_API_TOKEN = os.environ["INFERENCE_API_TOKEN"]
INFERENCE_MODEL = "gpt-4o-mini"


class Item(BaseModel):
    name: str
    price: float

    def __str__(self):
        return f"{self.name} : {self.price}"

    def __hash__(self):
        return str(self).lower().__hash__()

    def split(self):
        split_price = round(self.price / 2, 2)
        remaining_price = self.price - split_price

        split_item = Item(name=self.name, price=split_price)
        new_self = Item(name=self.name, price=remaining_price)

        return [new_self, split_item]


class Items(BaseModel):
    items: list[Item]

    def __str__(self):
        items = map(str, self.items)
        return "\n".join(items)

    def get_sum(self):
        prices = map(lambda item: item.price, self.items)
        return sum(prices)

    def split(self, item: int):
        split_items = self.items[item].split()
        self.items[item] = split_items.pop(0)
        if any(split_items):
            self.items.insert(item + 1, split_items[0])


def get_items(receipt_png_data: bytes) -> Items:
    client = OpenAI(api_key=INFERENCE_API_TOKEN)

    image = base64.b64encode(receipt_png_data).decode("utf-8")
    image_url = f"data:image/png;base64,{image}"

    messages = [
        {
            "role": "developer",
            "content": "You extract items from restaurant receipt images. "
            "The sum of the item prices should equal the subtotal amount written on the receipt.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Give me the list of item names and their prices.",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                },
            ],
        },
    ]

    response_format = Items

    response = client.beta.chat.completions.parse(
        model=INFERENCE_MODEL,
        messages=messages,
        response_format=response_format,
    )

    return response.choices[0].message.parsed
