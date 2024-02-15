from pydantic import BaseModel
from typing import List


class CheckListsItems(BaseModel):
    id: int
    description: str


class CheckLists(BaseModel):
    id: str
    items: List[CheckListsItems]
