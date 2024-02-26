from fastapi import Depends
from api.v1 import router
from auth.database import User
from auth.user_manager import current_active_user


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
