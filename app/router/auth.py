from fastapi import Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2,models,untils

router = APIRouter(
    tags = ["Authentication"]
)

# 创建用户登录接口
@router.post("/login")
def login_user(user_auth:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    print(user_auth)
    #使用orm查询数据信息
    user_msg = db.query(models.User).filter(models.User.email == user_auth.username).first()
    print(user_msg.password)
    if not user_msg:
        return {"data":"user not found"}
    
    if not untils.verify_password(user_auth.password,user_msg.password):
        return {"data":"password error"}
    access_token = oauth2.create_access_token(data={"user_id":user_msg.id})
    return {
        "type":"bearer",
        "token":access_token
    }