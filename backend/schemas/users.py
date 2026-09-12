from pydantic import BaseModel, Field
from typing import Optional
from pydantic.config import ConfigDict



class UserRequest(BaseModel):
    username: str
    password: str

#user_info对应的类
class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    #模型类配置
    model_config = ConfigDict(from_attributes=True)

#data数据模型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse=Field(..., alias="userInfo")

    #模型类配置
    model_config = ConfigDict(from_attributes=True,populate_by_name=True)

#更新用户信息的模型类
class UpdateUserInfoRequest(UserInfoBase):
    """
    更新用户信息请求模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")

class UserChangePasswordRequest(BaseModel):
    """
    用户修改密码请求模型
    """
    old_password: str=Field(...,alias="oldPassword",description="旧密码")
    new_password: str=Field(...,alias="newPassword",description="新密码")
