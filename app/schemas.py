from pydantic import BaseModel
from datetime import datetime

# 创建创建数据基础模型
class PostBase(BaseModel):
    title :str
    content:str
    published:bool = True


# 创建创建数据基础模型
class PostCreate(PostBase):
    pass

class UpdateCreate(BaseModel):
    title :str
    content:str
    published:bool = True

class Post(BaseModel):
    id:int
    title :str
    content:str
    published:bool = True
    created_at:datetime
    class Config:
        from_attributes = True