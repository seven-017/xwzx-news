from fastapi import FastAPI,Path,HTTPException
from routers import favorite, history, news, users
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handler import register_exception_handlers

app = FastAPI()
#注册异常处理函数
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,  # 允许跨域请求携带凭证
    allow_methods=["*"],    # 允许所有HTTP方法
    allow_headers=["*"],     # 允许所有请求头
)

@app.get("/")
async def root():
    return {"msg":"Hello World"}

#挂载路由/注册路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
