from pydantic import BaseModel, Field

class FavoriteRequest(BaseModel):
    """
    收藏新闻请求模型
    """
    is_favorite: bool=Field(...,alias="isFavorite")

class FavoriteAddRequest(BaseModel):
    """
    收藏新闻添加请求模型
    """
    news_id: int=Field(...,alias="newsId")