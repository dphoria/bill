import os
import base64
from typing import Iterable
from huggingface_hub import InferenceClient
from pydantic import BaseModel, PositiveInt, TypeAdapter
from typing import Optional
from logging import getLogger

log = getLogger(__file__)

HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]
HUGGINGFACEHUB_MODEL = "meta-llama/Llama-3.2-11B-Vision-Instruct"

class Item(BaseModel):
    name: str
    count: PositiveInt = 1
    price: float

def read_receipt(receipt_png_data: bytes) -> Iterable[str]:
    client = InferenceClient(api_key=HUGGINGFACEHUB_API_TOKEN)

    image = base64.b64encode(receipt_png_data).decode("utf-8")
    image = f"data:image/png;base64,{image}"

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text":
                        "Give me the list of every price and the corresponding name and count in this receipt image. "
                        "I want the list like this: "
                        "- name 1, count 1, price 1. "
                        "- name 2, count 2, price 2. "
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image
                    }
                }
            ]
        }
    ]

    completion = client.chat.completions.create(
        model=HUGGINGFACEHUB_MODEL, 
        messages=messages, 
        max_tokens=512,
        stream=True,
    )

    replies = map(lambda chunk: chunk.choices[0].delta.content, completion)
    yield from replies

def parse_item(receipt_line: str) -> Optional[Item]:
    receipt_line = receipt_line.strip()
    if not receipt_line.startswith("- "):
        return None

    fields = receipt_line.rsplit(",", 2)
    fields = [field.strip() for field in fields]
    fields[-1] = fields[-1].replace("$", "")
    keys = ["name", "count", "price"]

    try:
        return TypeAdapter(Item).validate_python(dict(zip(keys, fields)))
    except Exception:
        log.warning(f"not a receipt line: {receipt_line}")
        return None
