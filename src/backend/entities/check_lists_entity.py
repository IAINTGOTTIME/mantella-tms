from pydantic import BaseModel
from typing import List


class CheckListItem(BaseModel):
    id: int
    description: str


class CheckList(BaseModel):
    id: int
    items: List[CheckListItem]
