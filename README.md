# 雷普赛维（LABOR-SAVING）企业官网 · 前端

> 面向全国招商的机械臂厂家展示官网。Vue 3 + Vite 6 构建，**构建期预渲染**（SSG）输出真实 HTML 快照，满足百度/360/搜狗/Google 站长验证、结构化数据、llms.txt 等 SEO / GEO 硬指标。

---

## 一、项目简介

雷普赛维（LABOR-SAVING）是一家面向全国招募区域代理与经销商的工业机械臂生产厂家，主营产品为**助力机械臂、平衡吊、气动平衡器、伺服助力臂**，负载覆盖 50–600kg，适配汽车、3C 电子、家电、五金等行业的装配、上下料、码垛与移栽。

本仓库为官网**前端**工程（全栈项目中的 `frontend/` 模块），与 Django 后端（提供 `/api` 接口）及 SQLite 数据库（Navicat Premium Lite 管理）协同工作。前端以"接口优先 + 本地兜底"策略保证健壮性，并通过构建期预渲染让搜索引擎与 AI 引擎爬虫直接抓取到含正文的 HTML，规避纯 SPA 首屏空壳这一 GEO 死穴。

**品牌与合规要点**

- 品牌名：雷普赛维（LABOR-SAVING），强调色 `#e31c25`，黑底工业风。
- 全国招商，弱化地域权重（"辽宁/沈阳"仅作为关于页真实工商地址出现）。
- TDK（标题/关键词/描述）**禁止出现**「辽宁/沈阳」字样；招商文案**禁止**使用「稳赚/零风险/包赚」，表单与页面均带"投资有风险"提示。
- 全站禁用 Google Analytics 全站统计与 Google 字体（GTM 保留）；百度统计与百度自动推送仅在生产域名启用（localhost 自动跳过）。

---

## 二、技术栈

| 类别 | 选型 | 说明 |
| --- | --- | --- |
| 框架 | Vue 3.5（`script setup` + `<script setup>`） | 组合式 API |
| 构建 | Vite 6 | 开发/构建/预览 |
| 路由 | Vue Router 4（history 模式） | `createWebHistory` |
| 状态 | Pinia 2 | 站点配置等共享状态 |
| 请求 | Axios 1.7 | 统一封装 `/api` 代理与响应归一化 |
| 头部 | @vueuse/head 2.0 | TDK 与 JSON-LD 注入 |
| 预渲染 | puppeteer-core 23 + 系统 Chromium | 构建期 SSG |
| 包管理 | pnpm | `pnpm install` / `pnpm run <script>` |

---

## 三、目录结构

```
frontend/
├── index.html                 # SPA 入口模板（含 #app 挂载点、字体与 GTM 占位）
├── vite.config.js             # 别名 @、dev/preview 代理 /api 与 /media
├── package.json               # 脚本与依赖
├── pnpm-lock.yaml
├── scripts/
│   └── prerender.js           # 构建期预渲染脚本（puppeteer-core 抓取真实 DOM 落盘）
├── public/                    # 直接拷贝到 dist 根（不哈希）
│   ├── favicon.svg
│   ├── logo.svg
│   ├── robots.txt             # 含 GPTBot/PerplexityBot/Bytespider 等 AI 爬虫放行
│   ├── sitemap.xml            # 全站 URL 与优先级
│   └── llms.txt               # GEO 友好：供 AI 摘要引用的权威事实清单
└── src/
    ├── main.js                # 应用入口：pinia + head + router 注册
    ├── App.vue                # 布局骨架：Header / <main> / Footer / 悬浮电话
    ├── router/index.js        # 10 条路由 + 每路由 meta(TDK) + 百度自动提交
    ├── api/
    │   ├── index.js           # axios 实例、响应拦截、normalizeResponse
    │   └── content.js         # 站点/资讯/FAQ/招商/采购 业务接口（含 fallback）
    ├── stores/site.js         # Pinia：站点全局配置
    ├── composables/
    │   ├── useJsonLd.js       # onMounted 向 <head> 写入 application/ld+json
    │   ├── useTrack.js        # 百度统计 / GTM / lead_submit 埋点
    │   └── useLeadSource.js   # 识别线索来源 direct/search/ai/other
    ├── data/fallback.json     # 后端不可达时的本地兜底数据
    ├── assets/main.css        # 设计系统：CSS 变量、响应式断点、可访问性
    ├── components/            # 复用组件（见下表）
    └── views/                 # 页面视图（见下表）
```

**组件 `src/components/`**

| 组件 | 职责 |
| --- | --- |
| `SiteHeader.vue` | 吸顶导航，`max-width:1020px` 折叠为汉堡菜单 |
| `SiteFooter.vue` | 四栏页脚：品牌/导航/产品/联系 |
| `FloatPhone.vue` | 右下角悬浮电话（404 页隐藏） |
| `Breadcrumb.vue` | 面包屑（Product/News 详情页） |
| `LeadForm.vue` | 通用线索表单（招商/采购），含校验、蜜罐、埋点 |
| `FaqItem.vue` | 折叠式问答 |
| `ProductCard.vue` | 产品卡片 |
| `NewsCard.vue` | 资讯卡片 |
| `SectionCta.vue` | 行动召唤区块 |

**视图 `src/views/`**

`Home` · `Products` · `ProductDetail` · `Franchise` · `NewsList` · `NewsDetail` · `Faq` · `About` · `Contact` · `NotFound`

---

## 四、路由与页面

| 路由 | 名称 | 关键内容 / Schema |
| --- | --- | --- |
| `/` | Home | 首页（Organization）。预渲染后 HTML 含真实正文 |
| `/products` | Products | 三大系列总览 |
| `/products/:slug` | ProductDetail | `slug` ∈ {`balance-arm`, `pneumatic-balancer`, `servo-assist`}；注入 `Product` Schema |
| `/franchise` | Franchise | 招商政策、扶持、流程；`Service`+`Offer` Schema；招商表单 |
| `/news` | NewsList | 资讯列表（分页） |
| `/news/:slug` | NewsDetail | `slug` ∈ {`new-lightweight-arm`, `pneumatic-vs-servo`, `franchise-open`}；`Article` Schema |
| `/faq` | Faq | `FAQPage` Schema（JSON-LD 问答对） |
| `/about` | About | 企业简介（含真实工商地址），弱地域 |
| `/contact` | Contact | 联系方式与采购表单 |
| `*` | NotFound | 404（无悬浮电话） |

> 路由切换时（`router.afterEach`）触发百度自动链接提交（`zz.bdstatic.com/linksubmit/push.js`），且仅在生产域名执行。

---

## 五、API 契约（单一事实来源）

基础路径：`/api`。统一响应结构：**`{ code, data, msg }`**（注意是 `msg` 而非 `message`）。`code` 为 `0` 或 `200` 视为成功，由 `normalizeResponse` 解包出 `data`。

| 方法 | 端点 | 说明 | 失败兜底 |
| --- | --- | --- | --- |
| GET | `/site-config/` | 站点全局配置 | `fallback.json` → `siteConfig` |
| GET | `/news-categories/` | 资讯分类 | `fallback.json` → `newsCategories` |
| GET | `/news/` | 资讯列表（`?page=&category=`） | `fallback.json` → `newsList` |
| GET | `/news/:slug/` | 资讯详情 | `fallback.json` → `newsDetail` |
| GET | `/faqs/` | 常见问题 | `fallback.json` → `faqList` |
| POST | `/franchise/` | 招商线索提交 | 无兜底（直接抛出错误提示） |
| POST | `/purchase/` | 采购线索提交 | 无兜底 |

**表单提交约定**

- 后端会强制写入 `lead_type`（招商=`franchise` / 采购=`purchase`），**前端不可传该字段**。
- 前端**必须**携带：
  - `lead_source`：由 `useLeadSource.detect()` 识别（`direct` / `search` / `ai` / `other`）
  - `page_url`：当前页面 URL
- 其余字段：`name`、`phone`、`company`（选填）、`message`、`region`（招商）、`budget`（招商）、蜜罐 `honeypot`。
- 校验：姓名、电话（≥6 位数字）、留言、同意隐私政策必填；蜜罐有值则静默丢弃（防垃圾）。

开发期通过 `vite.config.js` 的 `server.proxy` 将 `/api` 与 `/media` 代理到 `http://127.0.0.1:8000`（Django 后端）。

---

## 六、SEO / GEO 策略

纯 SPA 首屏为空壳，是搜索引擎与 AI 引擎抓取的死穴。本工程以**构建期预渲染**解决：

1. **预渲染（SSG）**：`scripts/prerender.js` 启动 `vite preview`（显式绑定 `127.0.0.1`，避免 IPv6/IPv4 探测超时），用 puppeteer-core 调系统 Chromium 逐路由抓取 `networkidle0` 后的真实 DOM，落盘为 `dist/<route>/index.html`。共预渲染 14 条路由（含首页与 404）。
2. **结构化数据（JSON-LD）**：`useJsonLd.js` 在组件 `onMounted` 时向 `<head>` 写入，页面切换时自动清理。类型覆盖：全站 `Organization`、`/faq`→`FAQPage`、`/products/:slug`→`Product`、`/news/:slug`→`Article`、`/franchise`→`Service`+`Offer`，以及 `Breadcrumb`。
3. **TDK 独立**：每路由 `meta.title/keywords/description` 经 `@vueuse/head` 注入 `<title>` 与 `<meta>`。
4. **站长验证**：`fallback.json.siteConfig` 预留 `baidu_verify` / `qihoo_verify` / `sogou_verify` 字段，由后端注入到页面（`verify` 元标签 / 文件）。
5. **GEO 友好文件**：`public/robots.txt`（显式放行 GPTBot、PerplexityBot、Bytespider、CCBot 等）、`public/sitemap.xml`、`public/llms.txt`（供 AI 摘要引用的权威事实清单）。
6. **埋点**：`useTrack` 统一封装百度统计事件与 GTM `dataLayer` 推送；`lead_submit` 事件记录 `leadType` 与 `leadSource`。

> 验收对照：预渲染后首页 HTML ≈ 22KB、/faq ≈ 24KB，含真实正文与 JSON-LD，curl 即可取到非空壳页面。

---

## 七、设计系统（响应式 & 交互）

设计令牌集中在 `src/assets/main.css` 的 `:root`：

| 令牌 | 值 |
| --- | --- |
| 主背景 | `#0a0a0a` / `#111` / `#161616` |
| 强调红 | `#e31c25`（hover `#b7141b`） |
| 最大宽度 | `1200px` |
| 头部高度 | `72px`（移动端 `64px`） |

**响应式断点**

- `1020px`：导航折叠为汉堡抽屉菜单（`position:fixed` 下拉，`translateY` 过渡）。
- `680px`：栅格（grid-2/3/4）降为单列，间距与内边距收紧， speciation 表首列加宽。

**交互与可访问性**

- 流式字号：`clamp()` 实现标题自适应缩放。
- 焦点可见：`:focus-visible` 红色描边。
- 减少动画偏好：`prefers-reduced-motion` 降级过渡/动画。
- 表单：实时校验、错误内联提示、提交态禁用、成功态 `role=status`、错误 `role=alert`、蜜罐反爬。
- 悬浮电话：固定右下角，`transform` 微交互；404 页不渲染。

---

## 八、本地开发

前置：Node ≥ 18、pnpm、已运行的 Django 后端（`http://127.0.0.1:8000`）。

```bash
# 1. 安装依赖
pnpm install

# 2. 启动开发服务器（默认 http://localhost:5173，/api 代理到 8000）
pnpm dev

# 3. 预览生产构建（默认 http://localhost:4173）
pnpm preview
```

环境变量（可选）：

- `CHROME_BIN` / `CHROME_PATH`：预渲染使用的 Chromium 可执行文件路径，默认 `/usr/bin/chromium`。

---

## 九、构建与预渲染（部署前必做）

```bash
# 标准构建（仅 SPA，不含预渲染快照）
pnpm build

# 构建 + 构建期预渲染（推荐，用于生产部署）
pnpm build:prerender
```

`build:prerender` 等价于 `vite build` 后执行 `scripts/prerender.js`，最终 `dist/` 结构：

```
dist/
├── index.html              # 首页预渲染快照
├── about/index.html
├── products/index.html
├── products/balance-arm/index.html
├── products/pneumatic-balancer/index.html
├── products/servo-assist/index.html
├── franchise/index.html
├── news/index.html
├── news/new-lightweight-arm/index.html
├── news/pneumatic-vs-servo/index.html
├── news/franchise-open/index.html
├── faq/index.html
├── contact/index.html
├── 404/index.html
├── assets/                 # 哈希后的 JS / CSS
├── robots.txt / sitemap.xml / llms.txt / favicon.svg / logo.svg
```

部署时请将 `dist/` 整体上传到 Web 根，`/` 指向 `dist/index.html`，并为各 `<route>/index.html` 配置回退（SPA fallback）。`assets/` 下的 JS/CSS 带内容哈希，建议开启长缓存。

> 环境要求：预渲染依赖系统 Chromium。本工程使用 `puppeteer-core`（不自带浏览器），请确认 `CHROME_BIN` 指向有效 Chromium。常见路径：`/usr/bin/chromium` 或 `/opt/google/chrome/google-chrome`。

---

## 十、后端 / 数据库对接（Navicat Premium Lite）

- 数据库：SQLite（`db.sqlite3`），由 Django 管理。
- 管理工具：**Navicat Premium Lite**（免费版）连接本地 SQLite 文件即可查看/维护 `site_config`、`news`、`faq`、`franchise_lead`、`purchase_lead` 等表。
- 接口由 Django 提供，前端仅消费 `/api`（统一 `{code,data,msg}`）。新增字段时同步更新 `src/data/fallback.json`，保证后端不可达时仍有兜底展示。
- 招商/采购线索表（`franchise_lead` / `purchase_lead`）的 `lead_type` 由后端写入，前端提交时携带 `lead_source` 与 `page_url` 以便归因分析。

---

## 十一、合规检查清单（上线前）

- [ ] 全站 TDK 不含「辽宁/沈阳」
- [ ] 招商文案不含「稳赚/零风险/包赚」
- [ ] 招商表单与关键页面展示"投资有风险"提示
- [ ] 未启用 Google Analytics 全站统计；未引用 Google 字体
- [ ] 百度/360/搜狗验证元标签已注入（来自 `siteConfig`）
- [ ] `robots.txt`、`sitemap.xml`、`llms.txt` 已随 `dist` 发布且可访问
- [ ] 已执行 `pnpm build:prerender`，各路由 `index.html` 含真实正文与 JSON-LD
- [ ] 本地兜底 `fallback.json` 与后端契约一致

---

## 十二、常见问题

**Q：预渲染报「预览服务启动超时」？**
A：vite preview 默认绑定 `localhost`（解析为 IPv6 `::1`），而探测脚本用 IPv4 `127.0.0.1`。`scripts/prerender.js` 已用 `--host 127.0.0.1` 显式绑定修正，确保一致。

**Q：预渲染抓不到内容/空壳？**
A：确认 `CHROME_BIN` 指向有效 Chromium；检查 `vite preview` 是否正常返回页面；`page.goto` 使用 `waitUntil:'networkidle0'` 并在落盘前等待 800ms 让异步数据渲染完成。

**Q：后端没起时页面空白？**
A：接口层已对 GET 类接口配置 `.catch()` 兜底到 `fallback.json`，不会出现空白；POST 类（表单提交）无兜底，会向上抛出错误由表单组件提示。

**Q：如何改 TDK？**
A：编辑 `src/router/index.js` 中对应路由的 `meta.title/keywords/description`；动态内容（如资讯详情）在视图内用 `@vueuse/head` 覆盖。

---

*文档基于当前前端代码（版本 1.1.0）整理，作为前端工程的权威说明。后端接口以 `frontend-brief.md` 契约为准。*
