from fastapi import FastAPI, HTTPException,Response,status,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import oauth2,models,schemas
# 创建路由，并设置前缀
router = APIRouter(
    prefix= "/post"
)

#  查询接口
@router.get("/",response_model = List[schemas.Post])
def get_post(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # 使用orm查询数据库表
    posts = db.query(models.Post).all()
    return posts

# 创建接口
@router.post("/",response_model=schemas.Post)
def create_post(post :schemas.PostCreate,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # 使用orm创建数据信息
    print(current_user)
    posts = models.Post(title= post.title,content=post.content,published=post.published,owner_id=current_user.id)
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts

# 查看单独接口
@router.get("/{id}",response_model=schemas.Post,)
def get_one_post(id:int,response:Response,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # 使用orm查看单独数据信息
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data":"post not found"}
    return post

# 删除post中的数据
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,response:Response,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # 使用orm删除数据信息
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data":"post not found"}
    if post.owner_id != current_user.id:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"data":"you are not the user of this post"}
    db.delete(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# 更新post中的数据
@router.put("/{id}",response_model = schemas.Post)
def put_post(id:int,post:schemas.UpdateCreate,response:Response,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #使用orm进行数据更新
    posts_query = db.query(models.Post).filter(models.Post.id == id)
    posts_db= posts_query.first()
    if not posts_db:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data":"post not found"}
    if posts_query.owner_id != current_user.id:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"data":"you are not the user of this post"}
    posts_query.update(post.dict(), synchronize_session=False) 
    db.commit()
    db.refresh(posts_db)
    return posts_db