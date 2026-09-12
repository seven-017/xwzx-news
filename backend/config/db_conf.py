import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker

#加载项目根目录下的 .env 文件（该文件不会提交到 Git，见 .gitignore）
load_dotenv()

#数据库URL（从环境变量读取，避免账号密码写死在代码里）
ASYNC_DATABASE_URL = os.getenv("DATABASE_URL")
if not ASYNC_DATABASE_URL:
    raise RuntimeError("缺少环境变量 DATABASE_URL，请参考 .env.example 创建 .env 文件")

#创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

#创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

#依赖项，用于获取异步会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
