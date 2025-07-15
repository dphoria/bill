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

    def start_analysis(self) -> list:
        """
        Start analysis of the receipt image and return conversation messages.

        Returns
        -------
        list
            List of messages for continued conversation with the AI.
        """
        messages = [
            {
                "role": "system",
                "content": "You are an assistant that analyzes restaurant receipts. You can see the receipt image and will answer questions about it.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please read this receipt image. I'll ask you questions about it.",
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

        response = self.client.chat.completions.create(
            model=INFERENCE_MODEL, messages=messages
        )

        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )

        return messages

    def run_inference(self, messages: list, response_format: BaseModel) -> BaseModel:
        """
        Run inference on the provided messages using the OpenAI API and return the parsed response.

        Parameters
        ----------
        messages : list
            The conversation history to send to the model.
        response_format : BaseModel
            The Pydantic model to use for structured output.

        Returns
        -------
        BaseModel
            The parsed response from the model as an instance of the provided response_format.
        """
        response = self.client.beta.chat.completions.parse(
            model=INFERENCE_MODEL,
            messages=messages,
            response_format=response_format,
        )
        return response.choices[0].message.parsed
        response = self.client.beta.chat.completions.parse(
            model=INFERENCE_MODEL,
            messages=messages,
            response_format=response_format,
        )
        return response.choices[0].message.parsed

    def get_subtotal_with_chat(self, messages: list) -> tuple[Item, list]:
        """
        Extract subtotal using chat conversation with image uploaded once.

        Parameters
        ----------
        messages : list
            List of messages for continued conversation with the agent.

        Returns
        -------
        tuple[Item, list]
            A tuple containing the subtotal Item and updated messages list.
        """
        messages.append({"role": "user", "content": "What is the subtotal amount?"})

        response = self.run_inference(messages, Item)
        subtotal = response

        messages.append({"role": "assistant", "content": f"Subtotal: {subtotal.price}"})

        return subtotal, messages

    def get_items_with_chat(self, messages: list) -> tuple[Items, list]:
        """
        Extract items using chat conversation with image uploaded once.

        Parameters
        ----------
        messages : list
            List of messages for continued conversation with the agent.

        Returns
        -------
        tuple[Items, list]
            A tuple containing the Items collection and updated messages list.
        """
        messages.append(
            {
                "role": "user",
                "content": "What are the individual items and their prices? Give me the list of item names and their prices.",
            }
        )

        response = self.run_inference(messages, Items)
        items = response

        messages.append(
            {
                "role": "assistant",
                "content": f"Found {len(items.items)} items with total: {items.get_sum()}",
            }
        )

        return items, messages

    def get_service_charge_with_chat(self, messages: list) -> tuple[Item, list]:
        """
        Extract service charge using chat conversation with image uploaded once.

        Parameters
        ----------
        messages : list
            List of messages for continued conversation with the agent.

        Returns
        -------
        tuple[Item, list]
            A tuple containing the service charge Item and updated messages list.
        """
        messages.append(
            {
                "role": "user",
                "content": "What is the service charge, tip, or gratuity amount? If none is found, return 0.",
            }
        )

        response = self.run_inference(messages, Item)
        service_charge = response
        service_charge.name = "Service charge"

        messages.append(
            {"role": "assistant", "content": f"Service charge: {service_charge.price}"}
        )

        return service_charge, messages

    def get_tax_with_chat(self, messages: list) -> tuple[Item, list]:
        """
        Extract tax using chat conversation with image uploaded once.

        Parameters
        ----------
        messages : list
            List of messages for continued conversation with the agent.

        Returns
        -------
        tuple[Item, list]
            A tuple containing the tax Item and updated messages list.
        """
        messages.append({"role": "user", "content": "What is the tax amount?"})

        response = self.run_inference(messages, Item)
        tax = response

        messages.append({"role": "assistant", "content": f"Tax: {tax.price}"})

        return tax, messages
