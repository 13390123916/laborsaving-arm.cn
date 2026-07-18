# LABOR-SAVING 气动助力机械臂 - 前端

> Vue 3 + Vite 5 企业官网前端，SEO 优先，构建期预渲染（SSG）。

---

## 技术栈

| 类别 | 选型 | 说明 |
|------|------|------|
| 框架 | Vue 3 (`<script setup>`) | 组合式 API |
| 构建 | Vite 5 | 开发/构建/预览 |
| 路由 | Vue Router 4 (History 模式) | SPA 路由 |
| 请求 | Axios 1.7 | 统一封装 |
| 预渲染 | puppeteer-core + 系统 Chromium | 构建期 SSG |
| 包管理 | pnpm | `pnpm install` / `pnpm run <script>` |

## 目录结构

```
frontend/
├── index.html                 # SPA 入口（含验证 meta 标签占位）
├── vite.config.js             # API 代理 + 别名 + 预览代理
├── package.json               # 脚本与依赖
├── scripts/
│   ├── prerender.js           # Puppeteer 预渲染脚本
│   └── prerender.sh           # Shell 包装（启动 server → 渲染 → 关闭）
├── public/
│   ├── robots.txt             # 搜索引擎 + AI 爬虫规则
│   ├── sitemap.xml            # 站点地图
│   └── llms.txt               # AI 引擎引用清单
└── src/
    ├── main.js                # 应用入口
    ├── App.vue                # 布局骨架（导航/路由视图/页脚）
    ├── router/index.js        # 6 条路由 + 每路由独立 TDK
    ├── api/index.js           # Axios 封装 + 接口方法
    ├── plugins/seo.js         # SEO 插件（TDK/统计/验证/JSON-LD）
    ├── composables/
    │   └── useJsonLd.js       # JSON-LD 结构化数据注入
    ├── assets/style.css       # 全局样式
    └── views/
        ├── Home.vue           # 首页
        ├── About.vue          # 关于我们
        ├── News.vue           # 资讯列表
        ├── NewsDetail.vue     # 资讯详情
        ├── Faq.vue            # 常见问题
        └── Contact.vue        # 联系我们/表单
```

## 页面与路由

| 路由 | 名称 | 结构化数据 | 预渲染 |
|------|------|-----------|--------|
| `/` | 首页 | Organization Schema | ✅ |
| `/about` | 关于我们 | — | ✅ |
| `/news` | 资讯中心 | — | ✅ |
| `/news/:id` | 资讯详情 | Article Schema | ✅ (1-6) |
| `/faq` | 常见问题 | FAQPage Schema (15条问答对) | ✅ |
| `/contact` | 联系我们 | — | ✅ |

## 脚本命令

```bash
pnpm install           # 安装依赖
pnpm dev               # 开发模式 (端口 5173)
pnpm build             # 生产构建
pnpm build:prerender   # 构建 + SSG 预渲染
pnpm preview           # 预览构建产物 (端口 4173)
```

## 预渲染 (SSG)

构建期使用 Puppeteer-core 启动 Chromium，逐路由抓取 `networkidle0` 后的真实 DOM，输出为 `dist/<route>/index.html`。

**前置条件：** 系统需安装 Chromium（默认路径 `/usr/bin/chromium`，可通过 `CHROME_BIN` 环境变量覆盖）

**预渲染路由：** 共 11 条路由（首页 + 4 个主栏目 + 6 篇资讯详情）

后端需在 `127.0.0.1:8000` 运行（`vite preview` 通过代理转发 `/api` 请求）。

## SEO 策略

1. **SSG 预渲染**：解决 SPA 首屏空壳问题，搜索引擎爬虫直接获取含正文的 HTML
2. **结构化数据**：JSON-LD 注入到 `<head>`（Organization / FAQPage / Article）
3. **每路由独立 TDK**：router.afterEach 设置 title/keywords/description
4. **站长验证**：从后端 API 读取验证码，动态注入 `<meta>` 标签
5. **统计脚本**：百度统计 / 360 自动收录 / Google Analytics 按配置动态注入
6. **AI 友好**：`llms.txt` + 结构化数据 + FAQ 问答对

## 后端依赖

前端依赖 Django 后端运行在 `127.0.0.1:8000`，提供以下 API：

- `GET /api/site-config/info/` - 站点配置
- `GET /api/articles/` - 资讯列表
- `GET /api/articles/:id/` - 资讯详情
- `GET /api/faqs/` - FAQ 列表
- `POST /api/contacts/` - 提交表单
- `GET /api/products/` - 产品列表

---

*文档对应代码版本 1.0.0*
