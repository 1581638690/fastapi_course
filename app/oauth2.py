from datetime import datetime,timedelta,timezone
from . import schemas
import jwt
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import HTTPException,Depends
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 创建token
def create_access_token(data:dict,expires_delta:timedelta=None):
    to_data = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_data.update({"exp":expire})
    encoded_jwt = jwt.encode(to_data,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

# 解析token 获取用户信息
def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# 编写用户认证
def get_current_user(token:str = Depends(oauth2_scheme),credentials_exception = HTTPException(status_code=400,detail="Invalid Token",headers={"WWW-Authenticate":"Bearer"})):

    return verify_access_token(token,credentials_exception)
