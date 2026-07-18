# LABOR-SAVING 气动助力机械臂企业官网

> 全栈 SEO 优化企业展示官网 | Vue3 + Django + SQLite 完整闭环

---

## 项目简介

LABOR-SAVING 智能装备有限公司官方展示网站。主打 **SEO/搜索引擎收录优先**、**AI引擎友好**、**流量转化优先**，围绕百度、360、搜狗、Google 搜索引擎收录规则及 AI 大模型抓取规则优化。

全站采用 **前后端分离架构**（Vue3 + Django REST Framework），实现前台展示、后台管理、数据库存储、SEO 统计收录全闭环。

## 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| 前端 | Vue 3 + Vue Router 4 + Axios | 组合式 API，SPA 路由 |
| 构建 | Vite 5 | 开发/构建/预览 |
| 预渲染 | Puppeteer-core + Chromium | 构建期 SSG 输出真实 HTML 快照 |
| 后端 | Django 5 + Django REST Framework | RESTful API |
| 数据库 | SQLite | 轻量化数据存储 |
| 管理工具 | Navicat Premium Lite | 数据库可视化管理 |

## 目录结构

```
project/
├── frontend/                  # Vue3 前端工程
│   ├── index.html             # SPA 入口模板（含验证 meta 标签占位）
│   ├── vite.config.js         # Vite 配置 + API 代理 + 预览代理
│   ├── package.json           # 依赖与脚本
│   ├── scripts/
│   │   ├── prerender.js       # Puppeteer 构建期预渲染脚本
│   │   └── prerender.sh       # 预渲染入口 shell 包装
│   ├── public/
│   │   ├── robots.txt         # 爬虫规则（含 AI 爬虫放行）
│   │   ├── sitemap.xml        # 站点地图
│   │   └── llms.txt           # AI 引擎引用清单
│   └── src/
│       ├── main.js            # 应用入口
│       ├── App.vue            # 布局骨架（Header/Footer/路由视图）
│       ├── router/index.js    # 路由 + 每路由独立 TDK
│       ├── api/index.js       # Axios 封装 + API 接口方法
│       ├── plugins/seo.js     # SEO 插件（TDK注入/统计/验证/JSON-LD）
│       ├── composables/useJsonLd.js  # JSON-LD 结构化数据注入
│       ├── assets/style.css   # 全局样式（简约商务风/移动端自适应）
│       └── views/             # 页面视图
│           ├── Home.vue       # 首页（产品/优势/FAQ预览）
│           ├── About.vue      # 关于我们（企业实体信息）
│           ├── News.vue       # 资讯中心列表
│           ├── NewsDetail.vue # 资讯详情
│           ├── Faq.vue        # 常见问题（15条采购FAQ）
│           └── Contact.vue    # 联系我们（咨询表单）
├── backend/                   # Django 后端工程
│   ├── manage.py              # Django 管理入口
│   ├── requirements.txt       # Python 依赖
│   ├── config/
│   │   ├── settings.py        # 项目配置
│   │   ├── urls.py            # 根路由
│   │   └── wsgi.py            # WSGI 入口
│   └── api/
│       ├── models.py          # 数据模型（SiteConfig/Article/Faq/Contact/Product）
│       ├── views.py           # API 视图
│       ├── serializers.py     # 序列化器
│       ├── urls.py            # API 路由
│       ├── admin.py           # Django Admin 注册
│       └── init_data.py       # 初始化数据脚本
├── docs/                      # 文档
│   ├── API接口文档.md
│   ├── Navicat配置教程.md
│   ├── SEO配置说明.md
│   └── 部署文档.md
└── README.md                  # 本文件
```

## 快速开始

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py shell < api/init_data.py
python3 manage.py runserver 0.0.0.0:8000
```

### 前端启动

```bash
cd frontend
pnpm install
pnpm run dev          # 开发模式 (默认 :5173, API 代理到 :8000)
```

### 生产构建 + 预渲染

```bash
cd frontend
pnpm run build:prerender    # 构建 + SSG 预渲染
pnpm run preview            # 预览构建产物
```

## SEO 功能清单

### 搜索引擎收录

| 项目 | 技术实现 | 状态 |
|------|---------|------|
| 百度站长验证 | `<meta>` 标签 + SEO 插件动态注入 | ✅ |
| 百度统计 | `hm.baidu.com` 脚本动态注入 | ✅ |
| 百度链接自动推送 | `zz.bdstatic.com/push.js` | ✅ |
| 360 站长验证 | `<meta>` 标签动态注入 | ✅ |
| 360 自动收录 | `qhres2.com/sozz` 加载器 | ✅ |
| 搜狗站长验证 | `<meta>` 标签动态注入 | ✅ |
| Google 搜索验证 | `<meta>` 标签动态注入 | ✅ |
| Google Analytics | gtag.js 动态注入 | ✅ |
| SEO 结构化数据 | JSON-LD (Organization/FAQPage/Article) | ✅ |
| llms.txt | AI 引擎内容索引 | ✅ |
| robots.txt | 搜索引擎 + AI 爬虫规则 | ✅ |
| sitemap.xml | 全站 URL 提交 | ✅ |
| SSG 预渲染 | Puppeteer 构建期快照 (11 条路由) | ✅ |

### AI 引擎友好

- 全站结构化数据 (JSON-LD) 适配搜索引擎 AI 摘要
- FAQ 问答对 (`FAQPage` Schema) 直接输出到 HTML
- `llms.txt` 供 ChatGPT、Claude 等 AI 引擎直接引用
- SSG 预渲染确保 AI 爬虫抓取到含真实正文的页面

## API 接口

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/site-config/info/` | 站点配置 |
| GET | `/api/articles/` | 资讯列表（支持分类/分页） |
| GET | `/api/articles/categories/` | 资讯分类 |
| GET | `/api/articles/:id/` | 资讯详情 |
| GET | `/api/faqs/` | FAQ 列表（支持分类筛选） |
| POST | `/api/contacts/` | 提交咨询表单 |
| GET | `/api/contacts/stats/` | 表单统计 |
| GET | `/api/products/` | 产品列表 |

接口统一返回格式：`{ code, message, data }`

## 核心数据表

| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `site_config` | 站点全局配置 | 企业信息、SEO 验证码、统计 ID |
| `article` | 资讯/博客 | 独立 SEO TDK、分类、封面、内容 |
| `faq` | FAQ 问答 | 问题、答案、详细说明、分类、排序 |
| `contact` | 联系表单留言 | 姓名、电话、留言、IP、处理状态 |
| `product` | 产品 | 名称、图标、描述、分类、排序 |

## 数据库管理 (Navicat Premium Lite)

使用 Navicat Premium Lite 连接 `backend/db.sqlite3` 文件进行数据管理：
- 查看/编辑站点配置、FAQ、文章、产品数据
- 导出/备份数据
- 执行 SQL 查询
- 具体配置步骤见 `docs/Navicat配置教程.md`

## 合规说明

- 全站内容符合网络安全法要求，无违规/敏感/夸大内容
- 招商文案禁止使用"稳赚/零风险/包赚"等违规词汇
- 表单及关键页面展示"投资有风险"提示
- 全站 TDK 不含地域限制性词汇
- 使用百度统计等国内合规统计工具

## 部署

详情见 `docs/部署文档.md`

---

*项目版本 1.0.0 | 由 WorkBuddy AI Agent 构建*
