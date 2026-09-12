# xwzx-news

一个前后端分离的新闻资讯项目。后端提供 REST API，前端是移动端风格的 H5 应用。

| | 技术栈 |
|---|---|
| **后端** | FastAPI · SQLAlchemy 2.0 (async) · aiomysql · MySQL · passlib(bcrypt) · JWT |
| **前端** | Vue 3 · Vite 7 · Vant 4 · Pinia 3 · vue-router 4 · vue-i18n 9 · axios |

---

## 目录结构

```
xwzx-news/
├── backend/                 # 后端
│   ├── config/db_conf.py    # 数据库连接（从 .env 读取）
│   ├── models/              # ORM 模型：news.py / users.py
│   ├── schemas/             # Pydantic 请求/响应模型
│   ├── crud/                # 数据库操作：news.py / users.py
│   ├── routers/             # 路由：news.py / users.py
│   ├── utils/               # 鉴权、密码加密、统一响应、异常处理
│   ├── main.py              # 应用入口
│   ├── .env                 # 真实配置（不入库）
│   ├── .env.example         # 配置模板（入库）
│   └── requirements.txt
├── frontend/                # 前端
│   ├── src/
│   │   ├── config/api.js    # API 地址与 AI 配置（从 .env 读取）
│   │   ├── store/           # Pinia：user / news / favorite / history / theme / language
│   │   ├── views/           # 页面
│   │   ├── components/
│   │   ├── router/
│   │   └── i18n/            # 中英文
│   ├── .env                 # 真实配置（不入库）
│   └── .env.example         # 配置模板（入库）
├── start-backend.bat        # 启动后端
├── start-frontend.bat       # 启动前端
└── start-all.bat            # 一键启动两个服务
```

---

## 快速开始

### 前置条件

- Python 3.13
- Node.js 20 或更高
- MySQL 8，已创建数据库 `news_app`

### 1. 配置后端

复制 `backend/.env.example` 为 `backend/.env`，填入自己的数据库密码：

```
DATABASE_URL=mysql+aiomysql://root:你的密码@localhost:3306/news_app?charset=utf8mb4
```

### 2. 配置前端

复制 `frontend/.env.example` 为 `frontend/.env`，填入自己的 AI API Key
（到 <https://bailian.console.aliyun.com/> 申请）：

```
VITE_AI_API_KEY=sk-你自己的密钥
```

### 3. 启动

双击 `start-all.bat`，会自动打开两个窗口分别启动前后端。

也可以分开启动：

- `start-backend.bat` → <http://127.0.0.1:8000/docs>
- `start-frontend.bat` → <http://127.0.0.1:5173>

> 前端页面要能正常显示，**后端必须同时运行**——所有数据都靠后端接口。

---

## 接口一览

### 用户模块 `/api/user`

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/user/register` | 注册 |
| POST | `/api/user/login` | 登录，返回 token |
| GET | `/api/user/info` | 获取当前用户信息（需 token） |
| PUT | `/api/user/update` | 修改资料（需 token） |
| PUT | `/api/user/password` | 修改密码（需 token） |

### 新闻模块 `/api/news`

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/news/categories` | 新闻分类列表 |
| GET | `/api/news/list` | 新闻列表（分页） |
| GET | `/api/news/detail` | 新闻详情 |

### 收藏模块 `/api/favorite`

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/favorite/check` | 检查某条新闻是否已收藏（需 token） |
| POST | `/api/favorite/add` | 添加收藏（需 token） |

### 其他

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/` | 健康检查，返回 `{"msg": "Hello World"}` |

---

## 环境变量

所有敏感配置都放在 `.env` 里，**不进版本库**。仓库里只保留 `.env.example` 模板。

| 文件 | 变量 | 说明 |
|---|---|---|
| `backend/.env` | `DATABASE_URL` | 数据库连接串 |
| `frontend/.env` | `VITE_API_BASE_URL` | 后端地址 |
| `frontend/.env` | `VITE_AI_API_ENDPOINT` | 大模型 API 地址 |
| `frontend/.env` | `VITE_AI_API_KEY` | 大模型密钥 |
| `frontend/.env` | `VITE_AI_MODEL` | 使用的模型名 |

---

## 已完成

- 后端：用户注册 / 登录 / JWT 鉴权 / 改资料 / 改密码，新闻分类 / 列表 / 详情，收藏检查 / 添加
- 前端：登录、注册、首页、分类、详情、收藏、历史、我的、资料、设置、AI 对话共 11 个页面

## 待完成 / 可优化

- [ ] 收藏模块后端只做了 `check` / `add`，前端还调用了 `/api/favorite/remove`、`/api/favorite/list`、`/api/favorite/clear`，需要补齐
- [ ] `history` 模块后端尚未开始（前端 store 已在调用 `/api/history/*`，目前靠本地存储）
- [ ] `models/news.py` 与 `models/users.py` 各自定义了一个 `Base`，建议抽到 `models/base.py` 共用一个
- [ ] 建表方式目前是手动的，建议加 Alembic 迁移或启动时 `create_all`
- [ ] 后端补 `tests/` 测试用例
- [ ] 加上 CI 工作流


测试：这一行是练习用的