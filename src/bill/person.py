from pydantic import BaseModel
from typing import List


class Person(BaseModel):
    name: str
    items: List[int]
