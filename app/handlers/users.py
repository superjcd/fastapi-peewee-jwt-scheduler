from fastapi import APIRouter, Depends

from app.middlewares.deps import get_db
from app.middlewares.jwt_auth import get_auth_user

router = APIRouter(
    prefix="/users",
    dependencies=[Depends(get_db), Depends(get_auth_user)]
)


@router.get("/me")
def me():  
    """
    当前登录用户信息
    """
    return "you are authenticated"
