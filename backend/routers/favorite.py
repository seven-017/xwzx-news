from fastapi import APIRouter, Depends
from config.db_conf import get_db
from crud import favorite
from models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.favorite import FavoriteRequest
from utils.auth import get_current_user
from utils.response import success_response
from schemas.favorite import FavoriteAddRequest



router = APIRouter(prefix="/api/favorite",tags=["favorite"])


@router.get("/check")
async def check_favorite(news_id:int,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    is_favorite=await favorite.is_news_favorite(db,user.id,news_id)
    return success_response(message="检查收藏成功",data=FavoriteRequest(isFavorite=is_favorite))


@router.post("/add")
async def add_favorite(data:FavoriteAddRequest,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    result=await favorite.add_news_favorite(db,user.id,data.news_id)
    return success_response(message="收藏成功",data=result)

