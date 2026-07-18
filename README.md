# LABOR-SAVING 气动助力机械臂企业官网

> 全栈自适应 SEO 优化企业展示官网 · Vue3 + Django + SQLite 完整闭环

[![Vue3](https://img.shields.io/badge/Frontend-Vue3-42b883)](https://vuejs.org/)
[![Django](https://img.shields.io/badge/Backend-Django-0c4b33)](https://djangoproject.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003b57)](https://sqlite.org/)

**仓库地址**：[github.com/13390123916/laborsaving-arm.cn](https://github.com/13390123916/laborsaving-arm.cn)

---

## 项目简介

LABOR-SAVING 气动助力机械臂企业官网，主打 **搜索引擎收录优先、AI引擎友好、流量转化优先**。
全站代码、内容结构、页面布局均围绕百度、360、搜狗、Google 收录规则及 AI 大模型抓取规则优化。

### 核心特性

- ✅ **全平台收录优化**：百度/360/搜狗/Google 站长验证、统计代码、自动提交
- ✅ **AI 引擎友好**：llms.txt、Schema 结构化数据、FAQ 专属模块
- ✅ **功能闭环**：Vue3前台 + Django后台 + SQLite存储
- ✅ **移动端自适应**：100% 移动端适配，轻量化加载
- ✅ **转化追踪**：标准化咨询表单 + 转化事件埋点
- ✅ **企业背书**：关于页实体信用卡片强化

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vue Router + Vite |
| 后端 | Django 5 + Django REST Framework |
| 数据库 | SQLite |
| 工具 | Navicat Premium Lite |

---

## 目录结构

```
laborsaving-arm.cn/
├── backend/                 # Django 后端
│   ├── config/              # 项目配置（settings/urls/wsgi）
│   ├── api/                 # 应用（models/views/serializers/urls）
│   │   ├── models.py        # 数据库模型（5张核心表）
│   │   ├── views.py         # API 视图（RESTful）
│   │   ├── serializers.py   # 序列化器
│   │   ├── urls.py          # API 路由（/api/）
│   │   ├── seo_urls.py      # SEO 路由（llms/robots/sitemap/schema）
│   │   ├── admin.py         # 后台管理
│   │   ├── init_data.py     # 初始化数据（站点配置/15条FAQ/3篇资讯）
│   │   └── migrations/      # 数据库迁移文件
│   ├── manage.py
│   ├── requirements.txt
│   └── db.sqlite3           # 数据库文件（运行时生成）
├── frontend/                # Vue3 前端
│   ├── src/
│   │   ├── views/           # 页面组件（6个页面）
│   │   ├── api/             # API 封装（axios）
│   │   ├── router/          # 路由
│   │   ├── plugins/         # SEO 插件（TDK/统计代码）
│   │   └── assets/          # 全局样式
│   ├── package.json
│   ├── index.html           # 含站长验证meta标签
│   └── vite.config.js
└── docs/                    # 文档
    ├── SEO配置说明.md
    ├── Navicat配置教程.md
    ├── API接口文档.md
    └── 部署文档.md
```

---

## 快速启动

### 后端（Django）

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py shell < api/init_data.py   # 初始化数据
python manage.py runserver 0.0.0.0:8000
```

访问后台：`http://localhost:8000/admin/`（需先创建超级管理员）

### 前端（Vue3）

```bash
cd frontend
npm install
npm run dev        # 开发模式 http://localhost:5173
npm run build      # 生产构建到 dist/
```

### 创建后台管理员

```bash
cd backend
python manage.py createsuperuser
```

---

## 核心功能

| 模块 | 说明 |
|------|------|
| 首页 | Hero、核心产品、企业优势、FAQ预览、转化CTA |
| 关于我们 | 企业实体信用卡片、资质实力、服务范围、实景 |
| 资讯中心 | 分类筛选、列表、详情、独立TDK |
| FAQ | 15条采购高频问答，固定结构（问题→答案→详述），分类筛选 |
| 联系我们 | 咨询表单（姓名/电话/留言）、转化埋点、线索存储 |
| 后台管理 | 数据可视化增删改查（Django Admin） |

### 数据库表结构

| 表名 | 说明 | 关键字段 |
|------|------|----------|
| `user` | 用户表 | username, phone, department |
| `site_config` | 站点配置 | site_name, company_name, baidu_verify, baidu_tongji... |
| `article` | 资讯文章 | title, content, seo_title, views, status |
| `faq` | FAQ问答 | question, answer, detail, category |
| `contact` | 联系表单 | name, phone, message, is_handled |

---

## SEO 配置

详见 [docs/SEO配置说明.md](docs/SEO配置说明.md)

- 站长验证：百度/360/搜狗/Google
- 统计代码：百度统计/360收录/GTM/GA
- 结构化数据：Organization Schema、llms.txt、sitemap.xml、robots.txt
- 全站 TDK：每页独立配置

---

## 数据库管理

详见 [docs/Navicat配置教程.md](docs/Navicat配置教程.md)

使用 Navicat Premium Lite 连接 `backend/db.sqlite3`，进行表管理、数据增删改查、备份导出。

---

## 部署上线

详见 [docs/部署文档.md](docs/部署文档.md)

1. 前端 `npm run build` 生成静态文件
2. 静态文件部署至 Nginx / CDN
3. 后端使用 Gunicorn + Nginx 部署 Django
4. 配置域名解析至服务器
5. 各站长平台提交 sitemap.xml
6. 后台配置验证代码与统计 ID

---

## API 接口

详见 [docs/API接口文档.md](docs/API接口文档.md)

基础地址：`/api/`，统一返回格式 `{code, message, data}`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/site-config/info/` | GET | 获取站点配置 |
| `/articles/` | GET | 文章列表（支持分类/分页） |
| `/articles/{id}/` | GET | 文章详情（浏览量+1） |
| `/articles/categories/` | GET | 文章分类列表 |
| `/faqs/` | GET | FAQ列表（支持分类） |
| `/contacts/` | POST | 提交联系表单 |
| `/contacts/stats/` | GET | 线索统计 |

SEO 路由：`/llms.txt` · `/robots.txt` · `/sitemap.xml` · `/schema/organization.json`

---

## 许可证

本项目仅供企业官网建设学习与交流使用。

---

> **更新日期**：2026-07-18 · 全栈代码已推送至 GitHub 仓库
