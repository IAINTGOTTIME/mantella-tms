from fastapi import APIRouter

check_lists_router = APIRouter(
    tags=["check-lists"],
    prefix="/check-lists"
)


@check_lists_router.get("/")
def get_check_lists():
    pass


@check_lists_router.get("/{id}")
def get_one_check_list():
    pass


@check_lists_router.post("/")
def create_check_list():
    pass


@check_lists_router.put("/{id}")
def update_check_list():
    pass


@check_lists_router.delete("/{id}")
def delete_check_list():
    pass
