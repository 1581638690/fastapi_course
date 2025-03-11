from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import untils
from .. import schemas 
from .. import models

router = APIRouter(
    prefix="/user"
)

# 创建用户接口
@router.post("/",response_model = schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    # 使用orm创建数据信息
    # 添加密码加密
    user.password = untils.hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# 查询用户接口
@router.get("/{id}",response_model=schemas.UserOut)
def get_user_one(id:int,db:Session=Depends(get_db)):
    # 使用orm查询单个数据信息
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return {"data":"user not found"}
    return user