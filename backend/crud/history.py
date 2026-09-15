# 浏览历史模块：添加 / 获取列表 / 删除单条 / 清空
from sqlalchemy import delete, func, select

from models.news import News
from models.history import History
from sqlalchemy.ext.asyncio import AsyncSession


# 添加浏览记录
# 这块表没有 (user_id, news_id) 唯一约束（收藏表有，历史表故意没有），
# 所以"同一条新闻只留最新一次"要靠代码自己保证：
# 先删掉这条新闻的旧记录，再插入新记录 —— 效果就是重复浏览会把它顶到最前面。
async def add_news_history(db: AsyncSession, user_id: int, news_id: int):
    stmt = delete(History).where(History.user_id == user_id, History.news_id == news_id)
    await db.execute(stmt)

    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


# 获取浏览历史列表：当前用户的浏览记录 + 关联新闻信息 + 分页
async def get_news_history_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 50):
    # 总数
    count_query = select(func.count()).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one_or_none() or 0

    offset = (page - 1) * page_size
    # 列表查询：join 新闻表拿标题封面，按浏览时间倒序（最近看的在最前面）
    # 必须再加一个 id DESC 兜底：view_time 是 DATETIME 只精确到「秒」，
    # 如果同一秒内浏览了多篇（或测试时连续请求），只按 view_time 排顺序是随机的。
    # 因为我们 add 时是"先删旧记录再插新记录"，新记录的 id 一定更大，所以 id DESC 稳。
    # 查询结果形状：
    # [
    #     (新闻对象, 浏览时间, 历史ID),
    #     ...,
    # ]
    query = (select(News, History.view_time.label("view_time"), History.id.label("history_id"))
             .join(History, News.id == History.news_id)
             .where(History.user_id == user_id)
             .order_by(History.view_time.desc(), History.id.desc())
             .offset(offset)
             .limit(page_size)
             )
    result = await db.execute(query)
    # 取多列必须用 .all()，不能用 .scalars().all()
    # .scalars() 只会取每行的第一列，后面的浏览时间、历史ID 全丢了
    rows = result.all()
    return rows, total


# 删除单条浏览记录：按 新闻ID 删（前端的删除按钮传的就是新闻 id）
async def delete_news_history(db: AsyncSession, user_id: int, news_id: int):
    stmt = delete(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0  # 返回布尔值，True表示删除成功


# 清空浏览历史：删除当前用户的全部浏览记录
async def clear_news_history(db: AsyncSession, user_id: int):
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0  # 返回删除的行数，0表示本来就没有记录
