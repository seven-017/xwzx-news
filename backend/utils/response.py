from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message:str="success",data=None):
    content={
        "code":200,
        "msg":message,
        "data":jsonable_encoder(data) if data is not None else None
    }
    #目标：把任何的Fastapi，Pydantic，ORM对象都正常响应->code,message,data
    return JSONResponse(content=jsonable_encoder(content))
