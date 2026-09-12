from fastapi import Header,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud.users import get_user_by_token
from models.users import User
from config.db_conf import get_db
from fastapi import HTTPException,status


async def get_current_user(
        authorization: str=Header(...,alias="Authorization"),
        db: AsyncSession = Depends(get_db),
        ):
    token=authorization.removeprefix("Bearer ").strip()
    user=await get_user_by_token(db,token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="无效令牌或令牌过期")
    return user
     