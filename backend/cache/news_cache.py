from typing import List,Dict,Any
from config.cache_conf import get_json_cache, set_json_cache

CATEGORY_KEY = "news:categories"

#获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORY_KEY)

#写入新闻分类缓存：缓存的数据，过期时间。
#分类、配置7200；列表：600；详情：1800；验证码：120————数据越稳定，过期时间越长
#避免Key同时过期，引起雪崩
async def set_cached_categories(data: List[Dict[str, Any]],expire:int=7200):
    await set_json_cache(CATEGORY_KEY, data, expire)
