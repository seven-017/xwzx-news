
import json

import redis.asyncio as redis


#创建redis的连接对象
redis_client = redis.Redis(
    host='localhost', # redis的主机地址
    port=6379, # redis的端口号
    db=0,# 选择的数据库索引，默认是0
    decode_responses=True,# 是否将redis返回的字符串解码为python对象，默认是False
    #⚠️ 本机 Redis 服务端是 5.0.14，而 redis-py 8.x 默认用 RESP3 协议（会先发 HELLO 命令，
    #HELLO 是 Redis 6.0 才有的）。不指定 protocol=2 会直接报 unknown command `HELLO`。
    protocol=2
)

#设置和读取（字符串和列表或字典）
#读取：字符串
async def get_str(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"读取字符串失败：{e}")
        return None

#读取：列表或者字典
async def get_json_cache(key: str):
    try:
        #写入用的是 setex（Redis 的 String 类型），所以这里必须用 get 来读，
        #不能用 hgetall（那是读 Hash 类型的，两种结构在 Redis 里完全不是一回事）
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        else:
            return None
    except Exception as e:
        print(f"读取json缓存失败：{e}")
        return None

#设置缓存setex（key，expire，value）
async def set_json_cache(key: str, value: dict, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置json缓存失败：{e}")
        return None
    
