from sqlalchemy.ext.asyncio  import AsyncSession
from models.users import User
from sqlalchemy import select
from schemas.users import UserRequest
from utils import security
from datetime import datetime,timedelta
import uuid
from models.users import UserToken
from fastapi import HTTPException,status
from sqlalchemy import update,func
from schemas.users import UpdateUserInfoRequest,UserChangePasswordRequest


#根据用户名查询数据库
async def get_user_by_username(db:AsyncSession, username: str):
    stmt=select(User).where(User.username==username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

#创建用户
async def create_user(db:AsyncSession, user_data:UserRequest):
    #先密码加密处理->add
    hashed_password = security.hash_password(user_data.password)
    user=User(username=user_data.username,password=hashed_password)
    db.add(user) #添加到会话,不是IO操作,所以不需要await
    await db.commit()
    await db.refresh(user)
    return user

#生成token
async def create_token(db:AsyncSession, user_id:int):
    #生成token->设置过期时间->查询当前数据库是否有该token->有就更新,没有就创建
    token=str(uuid.uuid4())
    expires_at=datetime.now()+timedelta(days=7)
    query=select(UserToken).where(UserToken.user_id==user_id)
    result = await db.execute(query)
    token_record=result.scalar_one_or_none()
    if token_record:
        token_record.token=token
        token_record.expires_at=expires_at
    else:
        token_record=UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(token_record)
    await db.commit()
    await db.refresh(token_record)
    return token_record

async def anthenticate_user(db:AsyncSession, username:str,password:str):

    user = await get_user_by_username(db,username)
    if not user:
        return None
    if not security.verify_password(password,user.password):
        return None
    return user

#根据token查询用户:先查询token->判断token是否过期->根据token查询用户
async def get_user_by_token(db:AsyncSession, token:str):
    stmt=select(UserToken).where(UserToken.token==token)
    result = await db.execute(stmt)
    db_token=result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now():
        return None

    query=select(User).where(User.id==db_token.user_id)
    result = await db.execute(query)
    user=result.scalar_one_or_none()
    return user

#更新用户信息:update更新->检查是否命中->获取更新后的用户返回
async def update_user_info(db:AsyncSession, username:str, user_data:UpdateUserInfoRequest):
    #user_data是一个pydantic类型。转成字典，**解包
    #没有的字段,不会更新
    query=update(User).where(User.username==username).values(user_data.model_dump(exclude_unset=True,exclude_none=True))
    result = await db.execute(query)
    await db.commit()

    #检查更新
    if result.rowcount==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="用户不存在")

    #获取一下更新后的用户信息
    updated_user=await get_user_by_username(db,username)
    return updated_user

#修改密码；验证旧密码->更新新密码加密->返回成功响应
async def update_password(db:AsyncSession, user:User, username:str, user_data:UserChangePasswordRequest):
    if not security.verify_password(user_data.old_password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="旧密码错误")
    #更新新密码加密
    hashed_new_password=security.hash_password(user_data.new_password)
    user.password=hashed_new_password
    db.add(user)#更新：有SQLALchemy真正接管这个user对象，确保可以commit。避免session过期或者关闭导致不能提交
    await db.commit()
    await db.refresh(user)
    return True
   
