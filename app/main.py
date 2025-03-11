from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from .router import user,post
from .database import engine
from . import models
import psycopg2
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

app.include_router(user.router)
app.include_router(post.router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)