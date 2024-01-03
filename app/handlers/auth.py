from fastapi import APIRouter, Depends, Body
from starlette.responses import JSONResponse

from app.middlewares.deps import get_db
from app.schemas.auth import Token
from app.utils.auth import random_code_verifier
from app.services.auth import create_jwt_token_by_password, create_jwt_token_by_cellphone
from app.schemas.oauth2_schema import OAuth2PasswordRequest, OAuth2CellphoneRequest
from app.utils.sms import sms_sender
from app.utils.helper import is_chinese_cellphone

router = APIRouter(
    prefix="/auth",
    dependencies=[Depends(get_db)]
)

@router.post("/token", response_model=Token)
def token(request_data: OAuth2PasswordRequest):
    """
    用户名+密码登录
    """
    token = create_jwt_token_by_password(request_data)
    return {"token_type": "bearer", "token": token}


@router.post("/cellphone/token", response_model=Token)
def cellphone_token(request_data: OAuth2CellphoneRequest):
    """
    手机号+验证码登录
    """
    token = create_jwt_token_by_cellphone(request_data)
    return {"toekn_type": "bearer", "token": token}


@router.post("/cellphone/verification_code")
def send_verification_code(cellphone: str = Body(..., embed=True)):
    """
    发送验证码
    """
    if not is_chinese_cellphone(cellphone):
        return JSONResponse(status_code=422, content={"message": 'invalid cellphone'})

    code = random_code_verifier.make(cellphone)
    # fake send
    sms_sender.send(cellphone, {'code': code})
    return {"success": True}
