from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import history
from models.users import User
from schemas.history import HistoryAddRequest
from utils.auth import get_current_user
from utils.response import success_response


router = APIRouter(prefix="/api/history", tags=["history"])

# 前端 History.vue 是直接 {{ item.viewTime }} 插值的，所以在这里就格式化成好读的样子
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def _fmt(dt):
    """把 datetime 变成 '2026-09-15 10:43:20'，空值返回 None"""
    return dt.strftime(TIME_FORMAT) if dt else None


# 添加浏览记录
@router.post("/add")
async def add_history(
        data: HistoryAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    await history.add_news_history(db, user.id, data.news_id)
    return success_response(message="记录浏览历史成功", data=None)


# 获取浏览历史列表（带分页）
@router.get("/list")
async def get_history_list(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, alias="page"),
        page_size: int = Query(50, alias="pageSize", le=100)):
    rows, total = await history.get_news_history_list(db, user.id, page, page_size)

    # 注意这里的 news 是 News 的 ORM 对象，view_time 是 join 出来的浏览时间
    history_list = [{
        "id": news.id,
        "title": news.title,
        "description": news.description,
        "image": news.image,
        "author": news.author,
        "categoryId": news.category_id,
        "views": news.views,
        "publishTime": _fmt(news.publish_time),
        "viewTime": _fmt(view_time),
        "historyId": history_id,
    } for news, view_time, history_id in rows]

    has_more = total > page * page_size
    return success_response(message="获取浏览历史成功", data={
        "list": history_list,
        "total": total,
        "hasMore": has_more
    })


# 删除单条浏览记录
# 路径里的 {news_id} 传的是「新闻ID」，不是历史记录ID ——
# 前端 History.vue 的删除按钮绑的是 item.id，而这个 item 是新闻对象。
@router.delete("/delete/{news_id}")
async def delete_history(
        news_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    result = await history.delete_news_history(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="浏览记录不存在")
    return success_response(message="删除浏览记录成功", data=True)


# 清空浏览历史
@router.delete("/clear")
async def clear_history(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    count = await history.clear_news_history(db, user.id)
    return success_response(message=f"清空{count}条浏览记录", data=count)
