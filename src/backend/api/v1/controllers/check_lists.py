from typing import List

from fastapi import APIRouter, HTTPException

from entities.check_lists import CheckList, CheckListsItem

check_lists_router = APIRouter(
    tags=["check-lists"],
    prefix="/check-lists"
)

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
def create_check_list(new_item: CheckList):
    MOCK_CHECK_LISTS.append(new_item)
    return new_item


@check_lists_router.put("/{id}")
def update_check_list(id: str, new_item: CheckList):
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
