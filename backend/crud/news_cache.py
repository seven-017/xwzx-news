from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from cache.news_cache import set_cached_categories,get_cached_categories
from models.news import Category,News
from sqlalchemy import update

#旁路缓存策略
async def get_categories(db:AsyncSession,skip:int=0,limit:int=100):
    #从缓存中获取新闻分类
    cached_categories=await get_cached_categories()
    if cached_categories:
        return [Category(**d) for d in cached_categories]
    
    stmt=select(Category).offset(skip).limit(limit)
    result=await db.execute(stmt)
    categories=result.scalars().all()

    #将查询结果写入缓存
    if categories:
        #将分类转换为字典列表
        categories_data=jsonable_encoder(categories)
        await set_cached_categories(categories_data)

    return categories

async def get_news_list(db:AsyncSession,category_id:int,skip:int,limit:int):
    #根据分类ID查询新闻列表
    stmt=select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()

async def get_news_count(db:AsyncSession,category_id:int):
    stmt=select(func.count(News.id)).where(News.category_id==category_id)
    result=await db.execute(stmt)
    return result.scalar_one() #返回单个结果

async def get_news_detail(db:AsyncSession,news_id:int):
    stmt=select(News).where(News.id==news_id)
    result=await db.execute(stmt)
    return result.scalar_one_or_none() #返回单个结果或None

async def increase_news_views(db:AsyncSession,news_id:int):
    stmt=update(News).where(News.id==news_id).values(views=News.views+1)
    result=await db.execute(stmt)
    #await db.commit()

    #更新->检查数据库是否命中了数据->命中了返回True,否则返回False
    return result.rowcount>0

async def get_related_news(db:AsyncSession,category_id:int,news_id:int,limit:int=5):
    stmt=select(News).where(News.category_id==category_id,News.id!=news_id).order_by(News.views.desc(),News.publish_time.desc()).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()