# SEO 配置说明 - LABOR-SAVING 气动助力机械臂企业官网

本文档说明全站 SEO 配置项、站长验证、统计代码、结构化数据的部署方式。

---

## 一、站长验证配置

### 1. 百度站长
- **Meta验证**：在后台「站点配置」填写 `baidu_verify` 字段（格式如 `xxx123abc`）
- 前端 `index.html` 中已预留 `<meta name="baidu-site-verification">` 标签，后台配置后自动注入
- **百度统计**：填写 `baidu_tongji`（即 hm.js? 后的ID），前端 `src/plugins/seo.js` 自动加载 `hm.baidu.com/hm.js`
- **百度自动推送**：已默认集成 `zz.bdstatic.com/linksubmit/push.js`，每次页面加载自动推送链接

### 2. 360 站长
- **Meta验证**：后台填写 `qihu_verify` 字段
- **自动收录**：已默认加载 `qhres2.com/sozz` 自动收录脚本

### 3. 搜狗站长
- **Meta验证**：后台填写 `sogou_verify` 字段

### 4. Google
- **Meta验证**：后台填写 `google_verify` 字段
- **Google Analytics**：填写 `google_ga_id`
- **Google Ads**：填写 `google_ads_id`
- **GTM**：填写 `gtm_id`，前端自动加载 GTM 容器

---

## 二、结构化数据（Schema）

### 1. Organization Schema（首页）
首页通过 `useJsonLd.js` 在页面挂载时动态注入 `Organization` 类型 JSON-LD 到 `<head>`，包含：
- 企业名称、描述、成立时间
- 地址、联系方式
- 构建期预渲染后此 Schema 直接写入静态 HTML

### 2. FAQPage Schema（FAQ 页面）
FAQ 页面加载全部 15 条问答后，动态注入 `FAQPage` 类型 JSON-LD，每条问题作为 `Question`-`Answer` 问答对。

### 3. Article Schema（资讯详情页）
文章详情页注入 `Article` 类型结构化数据，包含标题、摘要、作者、发布时间、发布机构。

> 注意：所有 JSON-LD 通过前端 `useJsonLd.js` 组合式函数注入，组件卸载时自动清理，页面切换不会残留旧数据。预渲染后结构化数据直接写入静态 HTML，AI 爬虫无需执行 JS 即可识别。

---

## 三、AI 引擎友好配置

### llms.txt
访问根目录 `/llms.txt` 获取 AI 引擎友好索引文件，内容包含：
- 站点简介、核心产品、FAQ 摘要、企业信息、重要链接
- 适配 ChatGPT、Claude、文心一言等大模型引用

### robots.txt
已配置主流爬虫及 AI 爬虫（GPTBot、CCot、ChatGPT-User）允许抓取

### sitemap.xml
访问 `/sitemap.xml` 获取站点地图，包含静态页与文章页 URL

---

## 四、全站 TDK 配置

| 页面 | Title | Keywords | Description |
|------|-------|----------|-------------|
| 首页 | 后台 `site_title` | 后台 `site_keywords` | 后台 `site_description` |
| 关于 | 关于我们 - 站点名 | 企业名,企业简介 | 企业简介摘要 |
| 资讯列表 | 资讯中心 - 站点名 | 行业资讯,企业新闻 | 资讯列表描述 |
| 资讯详情 | 文章 `seo_title` | 文章 `seo_keywords` | 文章 `seo_description` |
| FAQ | 常见问题 - 站点名 | 机械臂问答,采购疑问 | FAQ描述 |
| 联系 | 联系我们 - 站点名 | 联系方式,咨询 | 联系描述 |

> 每篇文章独立 TDK 在后台「资讯文章」中配置，无重复、无空值。

---

## 六、构建期预渲染 (SSG)

构建时通过 Puppeteer-core 启动 Chromium，逐路由抓取 Vue SPA 的真实 DOM 并落盘为静态 HTML。

**作用：**
- 搜索引擎爬虫直接读取含正文的 HTML，无需执行 JavaScript
- AI 爬虫可抓取到结构化数据（JSON-LD）、FAQ 问答对等
- 解决纯 SPA 首屏空壳被搜索引擎判定为无内容的问题

**执行方式：**
```bash
cd frontend
pnpm run build:prerender
```

**预渲染路由（共 11 条）：**
`/`、`/about`、`/news`、`/news/1~6`、`/faq`、`/contact`

**前置条件：** Django 后端运行在 `127.0.0.1:8000`，系统安装 Chromium

---

## 七、转化事件埋点

联系表单提交时触发：
- 百度统计：`_hmt.push(['_trackEvent', 'form', 'submit', 'contact_form'])`
- GTM：`dataLayer.push({ event: 'form_submit', form_type: 'contact' })`

后端 `/api/contacts/stats/` 提供线索统计数据。

---

## 六、部署检查清单

- [ ] 后台配置所有站长验证代码
- [ ] 配置百度统计 ID
- [ ] 配置 GTM / GA ID
- [ ] 提交 sitemap.xml 到各站长平台
- [ ] 验证 llms.txt 可访问
- [ ] 各页面 TDK 无空值
- [ ] 移动端适配测试通过
