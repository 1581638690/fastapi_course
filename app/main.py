from fastapi import FastAPI
from .router import user,post,auth,vote
from .database import engine
from . import models
from fastapi.middleware.cors import CORSMiddleware
# 创建数据库表
#models.Base.metadata.create_all(bind=engine)




# 导入路由
app = FastAPI()
origins = [
   "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)