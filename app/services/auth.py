
from datetime import timedelta

from app.exceptions.exception import AuthenticationError
from app.models.user import User
from app.utils.auth import jwt_helper, hashing, random_code_verifier
from app.schemas.oauth2_schema import OAuth2CellphoneRequest, OAuth2PasswordRequest
from app.utils.helper import alphanumeric_random
from config.auth import settings



def create_jwt_token_by_password(data: OAuth2PasswordRequest):
    user = User.get_or_none(User.username == data.username)
    if not user:
        raise AuthenticationError(message='Incorrect email or password')

    # 用户密码校验
    if not (user.password and hashing.verify_password(data.password, user.password)):
        raise AuthenticationError(message='Incorrect email or password')

    # 用户状态校验
    if not user.is_enabled():
        raise AuthenticationError(message='Inactive user')
    
    expires_delta = timedelta(minutes=settings.JWT_TTL)
    token = jwt_helper.create_access_token(user.id, expires_delta)

    return token


def create_jwt_token_by_cellphone(data: OAuth2CellphoneRequest):
    cellphone = data.cellphone
    code = data.verification_code
    if not random_code_verifier.check(cellphone, code):
        raise AuthenticationError(message='Incorrect verification code')

    user = User.get_or_none(User.cellphone == cellphone)
    # 验证通过，用户不存在则创建
    if not user:
        username = 'srcp_' + alphanumeric_random()
        password = hashing.get_password_hash(alphanumeric_random())
        user = User.create(cellphone=cellphone, username=username, password=password)

    # 用户状态校验
    if not user.is_enabled():
        raise AuthenticationError(message='Inactive user')

    expires_delta = timedelta(minutes=settings.JWT_TTL)
    token = jwt_helper.create_access_token(user.id, expires_delta)

    return token

