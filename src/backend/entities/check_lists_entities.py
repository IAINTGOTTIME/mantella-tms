import uuid

from pydantic import BaseModel, UUID4
from typing import List
from uuid import UUID


class CheckListItem(BaseModel):
    id: int
    check_list_id: int
    description: str


class CheckList(BaseModel):
    id: int
    author_id: UUID
    change_from: UUID | None
    title: str
    items: List[CheckListItem]


class CheckListItemRequest(BaseModel):
    description: str


class CheckListRequest(BaseModel):
    title: str
    items: List[CheckListItemRequest]
