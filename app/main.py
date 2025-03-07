from fastapi import FastAPI, HTTPException,Response,status
from pydantic import BaseModel
from typing import Union,Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
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
    pubilshed:bool = True

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
    
#  查询接口
@app.get("/post")
def get_post():
    # 查询数据库表
    cursor.execute("select * from posts")
    data = cursor.fetchall()
    return {"data":data}

# 创建接口
@app.post("/post")
def create_post(post :Post):
    # post_dic = post.dict()
    # post_dic['id'] = randrange(0,1000000)
    # my_posts.append(post_dic)
    # 通过数据库添加数据信息
    cursor.execute("insert into posts(title,content,pubilshed) values(%s,%s,%s)",(post.title,post.content,post.pubilshed))
    conn.commit()
    cursor.execute("select * from posts")
    data = cursor.fetchall()

    return {"data":data}

# 查看单独接口
@app.get("/post/{id}")
def get_one_post(id:int,response:Response):
    # posts = find_id(id)
    # if not posts:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    cursor.execute("select * from posts where id = %s",(id,))
    data = cursor.fetchone()
    return {"data":data}

# 删除post中的数据
@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,response:Response):
    # index  = find_index(id)
    # 删除数据库表的数据 首先要判断他是否存在
    cursor.execute("select * from posts where id = %s",(id,))
    data = cursor.fetchone()
    if not data:
        response.status_code= status.HTTP_404_NOT_FOUND
        
    # 进行删除index
    cursor.execute("delete from posts where id =%s",(id,))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# 更新post中的数据
@app.put("/post/{id}")
def put_post(id:int,post:Post):
    #index = find_index(id)
    # 通过id查询数据库表
    cursor.execute("select * from posts where id = %s",(id,))
    data = cursor.fetchone()
    if not data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id :{id} does not exixt")
    cursor.execute("update posts set title = %s,content=%s,pubilshed=%s where id =%s",(post.title,post.content,post.pubilshed,id))
    conn.commit()
    cursor.execute("select * from posts")
    data = cursor.fetchall()
    return {"data":data}