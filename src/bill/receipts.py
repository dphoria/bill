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

        split_item = Item(name=f"{self.name} (2/2)", price=split_price)
        new_self = Item(name=f"{self.name} (1/2)", price=remaining_price)

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
        self.items[item] = split_items[0]
        self.items.insert(item + 1, split_items[1])


class Receipt:
    def __init__(self, receipt_png_data: bytes):
        """
        Initialize a Receipt instance with image data.

        Parameters
        ----------
        receipt_png_data : bytes
            Raw PNG image data of the receipt to be processed.

        Notes
        -----
        The image data is encoded to base64 and prepared for OpenAI API calls.
        An OpenAI client is initialized using the INFERENCE_API_TOKEN environment variable.
        """
        self.receipt_png_data = receipt_png_data
        self.client = OpenAI(api_key=INFERENCE_API_TOKEN)
        self.image = base64.b64encode(receipt_png_data).decode("utf-8")
        self.image_url = f"data:image/png;base64,{self.image}"

    def run_image_inference(
        self, developer_prompt: str, user_prompt: str, response_format: type
    ):
        """
        Run image inference using OpenAI's vision model.

        Parameters
        ----------
        developer_prompt : str
            System prompt that instructs the AI model on the task to perform.
        user_prompt : str
            User prompt that specifies what information to extract from the image.
        response_format : type
            Expected response format class (e.g., Items, Item).

        Returns
        -------
        Any
            Parsed response from the OpenAI API in the specified format.

        Notes
        -----
        This method constructs the messages for the OpenAI API call, including
        the image data encoded as base64, and returns the parsed response.
        """
        messages = [
            {
                "role": "developer",
                "content": developer_prompt,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": self.image_url,
                        },
                    },
                ],
            },
        ]

        response = self.client.beta.chat.completions.parse(
            model=INFERENCE_MODEL,
            messages=messages,
            response_format=response_format,
        )

        return response.choices[0].message.parsed

    def get_items(self) -> Items:
        """
        Extract individual items and their prices from the receipt image.

        Returns
        -------
        Items
            A collection of Item objects containing names and prices extracted
            from the receipt. The sum of item prices should equal the subtotal.
        """
        developer_prompt = "You extract items from restaurant receipt images. The sum of the item prices should equal the subtotal amount written on the receipt."
        user_prompt = "Give me the list of item names and their prices."
        return self.run_image_inference(developer_prompt, user_prompt, Items)

    def get_subtotal(self) -> Item:
        """
        Extract the subtotal amount from the receipt image.

        Returns
        -------
        Item
            An Item object with name "Subtotal" and the extracted subtotal amount
            as the price.
        """
        developer_prompt = "You extract the subtotal amount from restaurant receipt images. Look for the subtotal line item on the receipt and return it as an item with name 'Subtotal' and the amount as the price."
        user_prompt = "Give me the subtotal amount from this receipt."
        return self.run_image_inference(developer_prompt, user_prompt, Item)

    def get_tax(self) -> Item:
        """
        Extract the tax amount from the receipt image.

        Returns
        -------
        Item
            An Item object with name "Tax" and the extracted tax amount
            as the price.
        """
        developer_prompt = "You extract the tax amount from restaurant receipt images. Look for the tax line item on the receipt and return it as an item with name 'Tax' and the amount as the price."
        user_prompt = "Give me the tax amount from this receipt."
        return self.run_image_inference(developer_prompt, user_prompt, Item)

    def get_service_charge(self) -> Item:
        """
        Extract the service charge, tip, or gratuity amount from the receipt image.

        Returns
        -------
        Item
            An Item object with name "Service charge" and the extracted amount
            as the price. Returns 0.0 if no service charge, tip, or gratuity
            is found on the receipt.
        """
        developer_prompt = "You extract service charge, tip, or gratuity amounts from restaurant receipt images. Look for any line items labeled as tip, gratuity, or service charge on the receipt and return it as an item with name 'Service charge' and the amount as the price. If no such item is found, return an item with name 'Service charge' and price 0.0."
        user_prompt = "Give me the service charge, tip, or gratuity amount from this receipt. If none is found, return 0."
        return self.run_image_inference(developer_prompt, user_prompt, Item)
