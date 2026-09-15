from pydantic import BaseModel, ConfigDict, Field


class HistoryAddRequest(BaseModel):
    """
    添加浏览历史请求模型

    前端发的是 { newsId: 123 }，这里用 alias 接住，内部还是叫 news_id。
    """
    news_id: int = Field(..., alias="newsId", description="新闻ID")

    model_config = ConfigDict(
        populate_by_name=True,  # newsId 和 news_id 两种写法都收
    )


# 说明：列表接口没有配响应模型，直接返回手工拼的 dict。
# 原因是返回里带了"格式化好的时间字符串"，走 Pydantic 模型会被自动转回 ISO 格式
# （2026-09-15T10:43:20），前端 History.vue 是直接 {{ item.viewTime }} 插值的，不好看。
# 手工拼 dict 可以完全控制字段名和格式，代价是少了一层校验。
# 返回结构（前端契约，不能改）：
# {
#     "code": 200, "msg": "...",
#     "data": {
#         "list": [
#             {"id","title","description","image","author","categoryId",
#              "views","publishTime","viewTime"},
#             ...
#         ],
#         "total": 12,
#         "hasMore": false
#     }
# }
