from fastapi import APIRouter,HTTPException,Depends
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserRequest,UserAuthResponse  
from crud import users
from utils.response import success_response
from schemas.users import UserInfoResponse
from fastapi import status
from utils.auth import get_current_user
from models.users import User
from schemas.users import UpdateUserInfoRequest,UserChangePasswordRequest

router = APIRouter(prefix="/api/user",tags=["user"])

@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession=Depends(get_db)):

    existing_user = await users.get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=400,detail="用户名已存在")
    user = await users.create_user(db,user_data)
    token_record = await users.create_token(db,user.id)

    #验证用户名是否已存在->创建用户->生成token->返回token和用户信息
    # return {
    #     "code":200,
    #     "msg":"注册成功",
    #     "data":{
    #         "token":token_record,
    #         "userInfo":{
    #             "id":user.id,
    #             "username":user.username,
    #             "bio":user.bio,
    #             "avatar":user.avatar
    #         }
    #     }
    # }
    response_data=UserAuthResponse(token=token_record.token,user_info=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功",data=response_data)


@router.post("/login")
async def login(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    #登录逻辑：验证用户是否存在->验证密码是否正确->生成token->返回token和用户信息，响应结果
    user = await users.anthenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    token_record = await users.create_token(db,user.id)
    response_data=UserAuthResponse(token=token_record.token,user_info=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功",data=response_data)


#查token查用户->封装crud->工具整合成一个工具函数->路由导入使用：依赖注入
@router.get("/info")
async def get_user_info(user:User=Depends(get_current_user)):
    return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))

#修改用户信息：验证token->更新用户信息（用户输入数据put提交->请求体参数->定义pydantic模型）->返回成功响应
@router.put("/update")
async def update_user_info(user_data:UpdateUserInfoRequest,
                           user:User=Depends(get_current_user),
                           db:AsyncSession=Depends(get_db)):
    user=await users.update_user_info(db,user.username,user_data)
    return success_response(message="更新用户信息成功",data=UserInfoResponse.model_validate(user))

@router.put("/password")
async def update_password(user_data:UserChangePasswordRequest,
                           user:User=Depends(get_current_user),
                           db:AsyncSession=Depends(get_db)):
    res_change_pwd=await users.update_password(db,user,user.username,user_data)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="修改密码失败")
    return success_response(message="修改密码成功")
