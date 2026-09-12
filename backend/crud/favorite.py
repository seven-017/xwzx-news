

#检查收藏状态：当前用户是否收藏了这条新闻
from sqlalchemy import select

from models.favorite import Favorite
from sqlalchemy.ext.asyncio import AsyncSession


async def is_news_favorite(db: AsyncSession,user_id: int,news_id: int):
    query=select(Favorite).where(Favorite.user_id==user_id,Favorite.news_id==news_id)
    result=await db.execute(query)
    return result.scalar_one_or_none() is not None#返回布尔值，True表示收藏了，False表示没有收藏

async def add_news_favorite(db: AsyncSession,user_id: int,news_id: int):
    favorite=Favorite(user_id=user_id,news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite