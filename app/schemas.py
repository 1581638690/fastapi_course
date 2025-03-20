from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

# 创建创建数据基础模型
class PostBase(BaseModel):
    title :str
    content:str
    published:bool = True

# 创建创建数据基础模型
class PostCreate(PostBase):
    pass



# 创建用户模型pandic
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class UpdateCreate(BaseModel):
    title :str
    content:str
    published:bool = True


class UserCreate(BaseModel):
    email:EmailStr
    password:str


# 创建用户登录模型

class UserLogin(BaseModel):
    email:EmailStr
    password:str


# 创建用户登录模型
class TokenData(BaseModel):
    id: Optional[int] = None

# 创建token模型
class Token(BaseModel):
    access_token:str
    token_type:str