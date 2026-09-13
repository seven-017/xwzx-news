

#检查收藏状态：当前用户是否收藏了这条新闻
from sqlalchemy import delete, func, select

from models.news import News
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

async def remove_news_favorite(db: AsyncSession,user_id: int,news_id: int):
    stmt=delete(Favorite).where(Favorite.user_id==user_id,Favorite.news_id==news_id)
    result=await db.execute(stmt)
    await db.commit()
    return result.rowcount>0  #返回布尔值，True表示删除成功，False表示删除失败

#获取收藏列表：获取的是当前某个用户的收藏列表+分页功能
async def get_news_favorite_list(db: AsyncSession,user_id: int,page: int=1,page_size: int=10):
    #总量加收藏列表
    count_query=select(func.count()).where(Favorite.user_id==user_id)
    count_result=await db.execute(count_query)
    total=count_result.scalar_one_or_none()

    offset=(page-1)*page_size
    #获取收藏列表-列表查询join（）+收藏时间列表+分页
    #select（查询主体模型，字段别名）.join（联合查询的模型类，联合查询的条件）.where().order_by().offset().limit()
    # 查询结果：
    # [
    #     (新闻对象,收藏时间,收藏ID),
    #     ...,
    # ]
    query=(select(News,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id"))
            .join(Favorite,News.id==Favorite.news_id)
            .where(Favorite.user_id==user_id)
            .order_by(Favorite.created_at.desc())
            .offset(offset)
            .limit(page_size)
            )
    result=await db.execute(query)
    rows=result.scalars().all()
    return rows,total

#清空收藏列表：删除当前用户的收藏记录
async def clear_news_favorite(db: AsyncSession,user_id: int):
    stmt=delete(Favorite).where(Favorite.user_id==user_id)
    result=await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0  #返回删除的行数，0表示没有删除的记录
