from pydantic import BaseModel
from typing import List


class CheckListItem(BaseModel):
    id: int
    check_list_id: int
    description: str


class CheckList(BaseModel):
    id: int
    title: str
    items: List[CheckListItem]


class CheckListItemRequest(BaseModel):
    description: str


class CheckListRequest(BaseModel):
    title: str
    items: List[CheckListItemRequest]
