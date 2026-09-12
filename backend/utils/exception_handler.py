from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from utils.exception import sqlalchemy_error_handlar,generate_exception_handler,integrity_error_handlar,http_exception_handler



def register_exception_handlers(app):
    #注册异常处理函数
    app.add_exception_handler(SQLAlchemyError,sqlalchemy_error_handlar)#数据库
    app.add_exception_handler(Exception,generate_exception_handler)#其他异常
    app.add_exception_handler(IntegrityError,integrity_error_handlar)#数据完整性约束
    app.add_exception_handler(HTTPException,http_exception_handler)#HTTP异常