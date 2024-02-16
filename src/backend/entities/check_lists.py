from pydantic import BaseModel
from typing import List


<<<<<<< HEAD
class CheckListsItems(BaseModel):
=======
class CheckListsItem(BaseModel):
>>>>>>> origin/dev
    id: int
    description: str


<<<<<<< HEAD
class CheckLists(BaseModel):
    id: str
    items: List[CheckListsItems]
=======
class CheckList(BaseModel):
    id: str
    items: List[CheckListsItem]
>>>>>>> origin/dev
