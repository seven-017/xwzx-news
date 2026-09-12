from fastapi import APIRouter,Depends,Query,HTTPException
from config.db_conf import get_db
from crud import news
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import News

#创建apirouter实例
#prefix 路由前缀（api接口实例）
#tags 路由标签（用于分类）
router = APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_categories(skip:int=0,limit:int=100,db=Depends(get_db)):

    categories = await news.get_categories(db, skip, limit)
    return {
        "code":200,
        "msg":"获取分类成功",
        "data": categories
    }

@router.get("/list")
async def get_news_list(
    category_id:int=Query(...,alias="categoryId"),
    page:int=1,
    page_size:int=Query(10,alias="pageSize",le=100),
    db:AsyncSession=Depends(get_db)):
    #在这里调用crud层的函数获取新闻列表
    #news_list = await news.get_news_list(db, skip, limit)
    #思路：处理分页规则->查询新闻列表->查询总条数->判断是否有更多
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    has_more = (offset + page_size) < total
    return {
        "code":200,
        "msg":"获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
         #返回空列表，后续可以替换为实际数据
    }


@router.get("/detail")
async def get_news_detail(
    news_id:int=Query(...,alias="id"),
    db:AsyncSession=Depends(get_db)):
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")
    views_updated = await news.increase_news_views(db, news_id)
    if not views_updated:
        raise HTTPException(status_code=500, detail="更新浏览量失败")
    related_news = await news.get_related_news(db, news_detail.category_id, news_id)
    return {
        "code":200,
        "msg":"获取新闻详情成功",
        "data": {
            "id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publish_time":news_detail.publish_time,
            "category_id":news_detail.category_id,
            "views":news_detail.views,
            "relatedNews": related_news
        }
    }