from fastapi import FastAPI, HTTPException,Response,status,Depends
from pydantic import BaseModel
from typing import Union,Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

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

# 创建创建数据基础模型
class Post(BaseModel):
    title :str
    content:str
    published:bool = True

# 创建无数据库数据信息
my_posts = [
    {"title":"title of the 1","content":"content of the 1","id":1},
    {"title":"title of the 2","content":"content of the 2","id":2}
]

# 查询id
def find_id(id):
    for data in my_posts:
        if data["id"] == id:
            return data
        return {}

# 写出删除id的index
def find_index(id):
    for data in my_posts:
        if data["id"] == id:
            return my_posts.index(data)
# 测试sql
@app.get("/sqlalchemy")
def get_sqlalchemy(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message":"hello sqlalchemy"}


#  查询接口
@app.get("/post")
def get_post(db:Session = Depends(get_db)):
    # 使用orm查询数据库表
    posts = db.query(models.Post).all()
    return {"data":posts}

# 创建接口
@app.post("/post")
def create_post(post :Post,db:Session = Depends(get_db)):

    # 使用orm创建数据信息
    post = models.Post(title= post.title,content=post.content,published=post.published)
    db.add(post)
    db.commit()
    return {"data":"successfully created post"}

# 查看单独接口
@app.get("/post/{id}")
def get_one_post(id:int,response:Response,db:Session = Depends(get_db)):
    # 使用orm查看单独数据信息
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data":"post not found"}
    return {"data":post}

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
@app.put("/post/{id}")
def put_post(id:int,post:Post,response:Response,db:Session = Depends(get_db)):
    #使用orm进行数据更新
    posts = db.query(models.Post).filter(models.Post.id == id).update(post.dict())
    if not posts:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data":"post not found"}
    
    db.commit()
    return {"data":"update data successfully"}