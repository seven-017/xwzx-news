from datetime import datetime
from sqlalchemy import Index, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from models.news import News
from models.users import User


class Base(DeclarativeBase):
    pass


class History(Base):
    """
    浏览历史表ORM模型

    注意：这里单独定义 Base，不继承 models.news 的 Base。
    因为那个 Base 里带 created_at / updated_at 两列，而 history 表没这两列，
    继承过来会多查不存在的字段直接报错。
    """
    __tablename__ = 'history'

    # 创建索引
    __table_args__ = (
        Index('fk_history_user_idx', 'user_id'),
        Index('fk_history_news_idx', 'news_id'),
        Index('idx_view_time', 'view_time'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="历史ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="新闻ID")
    # 用 datetime.now（本地时间），不用 utcnow，否则页面上的浏览时间会差 8 小时
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="浏览时间")

    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})>"
