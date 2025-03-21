from fastapi import Response,status,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2,models,schemas

router = APIRouter(
    prefix= "/vote"
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_vote(vote:schemas.Vote,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        return {"data":"文章不存在"}
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    vote_one = vote_query.first()
    # 如果dir为1则为点赞，如果dir为0则为取消点赞
    if vote.dir == 1:
        # 点赞
        #vote_one = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id).first()
        if vote_one:
            return {"data":"你已经点过赞了！！"}
        # 否则就是未点赞
        vote = models.Vote(post_id = vote.post_id,user_id = current_user.id)
        db.add(vote)
        db.commit()
        db.refresh(vote)
        return vote
    else:
        # 取消点赞
        #vote_one = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id).first()
        if not vote_one:
            return {"data":"你还没有点过赞！！"}
        db.delete(vote_one)
        db.commit()
        return {"data":"取消点赞成功！！"}