from typing import List

from fastapi import APIRouter, HTTPException

<<<<<<< HEAD
from entities.check_lists import CheckLists, CheckListsItems
=======
from entities.check_lists import CheckList, CheckListsItem
>>>>>>> origin/dev

check_lists_router = APIRouter(
    tags=["check-lists"],
    prefix="/check-lists"
)

<<<<<<< HEAD
MOCK_CHECK_LISTS: List[CheckLists] = [
    CheckLists(
        id="1",
        items=[CheckListsItems(id=1, description="dasdasdasd321312312312"),
               CheckListsItems(id=2, description="dasdasdasd2313132313"),
               CheckListsItems(id=3, description="dasdasdasdASAADADADS"),
               CheckListsItems(id=4, description="dasdasdadfg"),
               CheckListsItems(id=5, description="dasdasd321"),
               ]
    ),
    CheckLists(
        id="2",
        items=[CheckListsItems(id=1, description="dasdasdasd321312312312"),

               ]
    ),
    CheckLists(
        id="3",
        items=[CheckListsItems(id=1, description="dasdasdasd321312312312"),
               CheckListsItems(id=4, description="dasdasdadfg"),
               CheckListsItems(id=5, description="dasdasd321"),
               ]
    ),

    CheckLists(
        id="4",
        items=[CheckListsItems(id=1, description="dasdasdasd321312312312"),
               CheckListsItems(id=2, description="dasdasdasd2313132313"),
               CheckListsItems(id=3, description="dasdasdasdASAADADADS"),
=======
MOCK_CHECK_LISTS: List[CheckList] = [
    CheckList(
        id="1",
        items=[CheckListsItem(id=1, description="dasdasdasd321312312312"),
               CheckListsItem(id=2, description="dasdasdasd2313132313"),
               CheckListsItem(id=3, description="dasdasdasdASAADADADS"),
               CheckListsItem(id=4, description="dasdasdadfg"),
               CheckListsItem(id=5, description="dasdasd321"),
               CheckListsItem(id=6, description="dasdasd321"),
               ]
    ),
    CheckList(
        id="2",
        items=[CheckListsItem(id=1, description="dasdasdasd321312312312"),

               ]
    ),
    CheckList(
        id="3",
        items=[CheckListsItem(id=1, description="dasdasdasd321312312312"),
               CheckListsItem(id=4, description="dasdasdadfg"),
               CheckListsItem(id=5, description="dasdasd321"),
               ]
    ),

    CheckList(
        id="4",
        items=[CheckListsItem(id=1, description="dasdasdasd321312312312"),
               CheckListsItem(id=2, description="dasdasdasd2313132313"),
               CheckListsItem(id=3, description="dasdasdasdASAADADADS"),
>>>>>>> origin/dev

               ]
    )
]


@check_lists_router.get("/")
def get_check_lists():
    return MOCK_CHECK_LISTS


@check_lists_router.get("/{id}")
def get_one_check_list(id: str):
    for check_lists in MOCK_CHECK_LISTS:
        if check_lists.id == id:
            return check_lists
    raise HTTPException(status_code=404, detail=f"check lists with id {id} not found")


@check_lists_router.post("/")
<<<<<<< HEAD
def create_check_list(new_item: CheckLists):
=======
def create_check_list(new_item: CheckList):
>>>>>>> origin/dev
    MOCK_CHECK_LISTS.append(new_item)
    return new_item


@check_lists_router.put("/{id}")
<<<<<<< HEAD
def update_check_list(id: str, new_item: CheckLists):
=======
def update_check_list(id: str, new_item: CheckList):
>>>>>>> origin/dev
    for i, check_lists in enumerate(MOCK_CHECK_LISTS):
        if check_lists.id == id:
            MOCK_CHECK_LISTS[i] = new_item
            return MOCK_CHECK_LISTS[i]
        raise HTTPException(status_code=404, detail=f"check lists with id {id} not found")


@check_lists_router.delete("/{id}")
def delete_check_list(id: str):
    for check_lists in MOCK_CHECK_LISTS:
        if check_lists.id == id:
            MOCK_CHECK_LISTS.remove(check_lists)
            return
        raise HTTPException(status_code=404, detail=f"check lists with id {id} not found")
