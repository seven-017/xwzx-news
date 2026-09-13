from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.base import NewsItemBase

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

class FavoriteItemResponse(NewsItemBase):
    favorite_time:datetime=Field(alias="favoriteTime")
    favorite_id:int=Field(alias="favoriteId")

    model_config=ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

class FavoriteListResponse(BaseModel):
    list:list[FavoriteItemResponse]
    total:int
    has_more:bool=Field(alias="hasMore")

    model_config=ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )