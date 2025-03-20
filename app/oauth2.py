from datetime import datetime,timedelta,timezone
from . import schemas,models
import jwt
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # 让fastapi知道我们token的位置
# 编写用户认证
def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    print(f"DEBUG: Received token = {token}") 
    credentials_exception = HTTPException(
        status_code=400, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"}
    )
    token_data = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user
