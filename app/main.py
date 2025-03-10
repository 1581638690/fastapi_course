from fastapi import FastAPI, HTTPException,Response,status,Depends

from typing import Union,Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .import schemas 
from .database import engine, get_db
from . import models
from sqlalchemy.orm import Session
# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 导入sql链接
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="123456",
            port="5433",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        break
    except Exception as e:
        print(f"数据库链接失败，正在重试，{e}".format(e))


# 导入路由
app = FastAPI()

#  查询接口
@app.get("/post",response_model = List[schemas.Post])
def get_post(db:Session = Depends(get_db)):
    # 使用orm查询数据库表
    posts = db.query(models.Post).all()
    return posts

# 创建接口
@app.post("/post",response_model=schemas.Post)
def create_post(post :schemas.PostCreate,db:Session = Depends(get_db)):

    # 使用orm创建数据信息
    posts = models.Post(title= post.title,content=post.content,published=post.published)
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts

# 查看单独接口
@app.get("/post/{id}",response_model=schemas.Post)
def get_one_post(id:int,response:Response,db:Session = Depends(get_db)):
    # 使用orm查看单独数据信息
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data":"post not found"}
    return post

# 删除post中的数据
@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,response:Response,db:Session = Depends(get_db)):
    # 使用orm删除数据信息
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data":"post not found"}
    db.delete(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# 更新post中的数据
@app.put("/post/{id}",response_model = schemas.Post)
def put_post(id:int,post:schemas.UpdateCreate,response:Response,db:Session = Depends(get_db)):
    #使用orm进行数据更新
    posts_query = db.query(models.Post).filter(models.Post.id == id)
    posts_db= posts_query.first()
    if not posts_db:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data":"post not found"}
    posts_query.update(post.dict(), synchronize_session=False) 
    db.commit()
    db.refresh(posts_db)
    return posts_db