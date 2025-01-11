import os
import base64
from typing import Iterable
from openai import OpenAI
from pydantic import BaseModel
from logging import getLogger

log = getLogger(__file__)

INFERENCE_API_TOKEN = os.environ["INFERENCE_API_TOKEN"]
INFERENCE_MODEL = "gpt-4o-mini"


class Item(BaseModel):
    name: str
    count: int
    price: float

    def __str__(self):
        return f"{self.name} ({self.count}) : {self.price}"


class Items(BaseModel):
    items: list[Item]


def get_items(receipt_png_data: bytes) -> Iterable[Item]:
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
                    "text": "Give me the list of item names, their counts and their prices.",
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

    yield from response.choices[0].message.parsed.items
