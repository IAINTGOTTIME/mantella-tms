from pydantic import BaseModel
from typing import List


class CheckListsItem(BaseModel):
    id: int
    description: str


class CheckList(BaseModel):
    id: str
    items: List[CheckListsItem]
