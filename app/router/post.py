from fastapi import Response,status,Depends,APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List,Optional
from ..database import get_db
from .. import oauth2,models,schemas
# 创建路由，并设置前缀
router = APIRouter(
    prefix= "/post"
)
#  查询接口
@router.get("/",response_model = List[schemas.postOut])
def get_post(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit:int =10,skip:int=0,search:Optional[str]=""):
    # 使用orm查询所有数据库表
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts =db.query(models.Post).filter(models.Post.owner_id == current_user.id,
                                        models.Post.title.contains(search)).limit(limit).all()
    #  使用orm查询所有的帖子，并且带有点赞数 需要展示出来
    votes_posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id,
                                        models.Post.title.contains(search)).limit(limit).all()
    
    return votes_posts

# 创建接口
@router.post("/",response_model=schemas.Post)
def create_post(post :schemas.PostCreate,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # 使用orm创建数据信息
    posts = models.Post(title= post.title,content=post.content,published=post.published,owner_id=current_user.id)
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts

# 查看单独接口
@router.get("/{id}",response_model=schemas.postOut)
def get_one_post(id:int,response:Response,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # 使用orm查看单独数据信息
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id and models.Post.owner_id==current_user.id).first()
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