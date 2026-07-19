# SEO 配置说明 - LABOR-SAVING 气动助力机械臂企业官网

> 域名：`laborsaving-arm.cn` ｜ 备案：管局审核中（验证/统计凭证待上线填）
> 本文档说明全站 SEO 配置项、站长验证、统计代码、结构化数据的部署方式。

---

## 一、站长验证配置

### 1. 百度站长
- **Meta 验证**：后台「站点配置」填写 `baidu_verify`（格式如 `xxx123abc`）
- 前端 `index.html` 预留 `<meta name="baidu-site-verification">`，配置后自动注入
- **百度统计**：填写 `baidu_tongji`（即 `hm.js?` 后的 ID），前端 `seo.js` 自动加载 `hm.baidu.com/hm.js`
- **百度主动推送**：默认集成 `zz.bdstatic.com/linksubmit/push.js`，每次页面加载自动推送链接

### 2. 360 站长
- **Meta 验证**：后台填写 `qihu_verify`
- **自动收录**：`qihu_push_url` 为**后台配置项**——上线后在「站点配置」填入 360 站长平台最新 sozz 脚本地址；**留空则不加载**，避免失效死链 404（`seo.js` 对空值不加载）

### 3. 搜狗站长
- **Meta 验证**：后台填写 `sogou_verify`

### 4. Google
- **Meta 验证**：后台填写 `google_verify`
- **Google Analytics 4**：填写 `google_ga_id`
- **Google Ads**：填写 `google_ads_id`
- **GTM**：填写 `gtm_id`，前端自动加载 GTM 容器

---

## 二、上线前必须替换的占位值（关键）

> 当前 `SiteConfig` 中以下字段为**占位符**，必须在备案通过、域名上线后，到各站长平台获取真实值填入后台「站点配置」，否则搜索引擎无法验证、统计为零：

| 字段 | 平台 | 获取位置 |
|------|------|----------|
| `baidu_verify` | 百度搜索资源平台 | 站点管理 → 验证 → meta 标签内容 |
| `baidu_tongji` | 百度统计 | 网站首页代码 `hm.js?` 后的 ID |
| `baidu_push_token` | 百度搜索资源平台 | 链接提交 → 主动推送 → 接口调用地址中的 token |
| `qihu_verify` | 360 站长平台 | 站点验证 → meta 内容 |
| `qihu_push_url` | 360 站长平台 | 自动收录 → 最新 sozz 脚本 URL |
| `sogou_verify` | 搜狗站长平台 | 验证 → meta 内容 |
| `google_verify` | Google Search Console | 资源设置 → 验证 → HTML 标记内容 |
| `google_ga_id` | Google Analytics | 数据流 → 测量 ID（G-xxxx） |
| `gtm_id` | Google Tag Manager | 容器 ID（GTM-xxxx） |

> 所有字段经 `seo.js` 动态注入 `<meta>` 与统计脚本；空值不加载，安全无死链。

---

## 三、结构化数据（Schema）

### 1. Organization / LocalBusiness（首页 + 关于页 + 联系页）
通过 `useJsonLd.js` 在页面挂载时注入 `LocalBusiness` 类型 JSON-LD，含企业名称、地址 GEO 坐标、联系方式。

### 2. FAQPage（FAQ 页面）
加载全部问答后动态注入 `FAQPage` JSON-LD（15+ 问答对，问题→答案→详情）。

### 3. Article（资讯详情页）
注入 `Article` JSON-LD（标题、摘要、作者、发布时间、发布机构）。

> 所有 JSON-LD 经 `useJsonLd.js` 注入，组件卸载自动清理；预渲染后直接写入静态 HTML，AI 爬虫无需执行 JS 即可识别。

---

## 四、AI 引擎友好配置

- **llms.txt**：根目录 `/llms.txt` 动态生成，含站点简介、核心产品、FAQ、企业信息、重要链接，供 ChatGPT、Claude、文心一言等引用
- **robots.txt**：放行百度/Google 及 AI 爬虫（GPTBot、CCBot、ChatGPT-User）
- **sitemap.xml**：含静态页 + 文章页 URL（动态生成，含最新文章）

---

## 五、全站 TDK 配置

| 页面 | Title | Keywords | Description |
|------|-------|----------|-------------|
| 首页 | 后台 `site_title` | 后台 `site_keywords` | 后台 `site_description` |
| 关于 | 关于我们 + 站点名 | 企业名,企业简介 | 企业简介摘要 |
| 资讯列表 | 资讯中心 + 站点名 | 行业资讯,企业新闻 | 资讯列表描述 |
| 资讯详情 | 文章 `seo_title` | 文章 `seo_keywords` | 文章 `seo_description` |
| FAQ | 常见问题 + 站点名 | 机械臂问答,采购疑问 | FAQ 描述 |
| 联系 | 联系我们 + 站点名 | 联系方式,咨询 | 联系描述 |

> 每篇文章独立 TDK（`init_data.py` 中每篇可带 `seo_title/seo_keywords/seo_description`，缺失回退默认），无重复、无空值。

---

## 六、构建期预渲染（SSG）

```bash
cd frontend
pnpm run build:prerender
```

预渲染路由（共 11 条）：`/`、`/about`、`/news`、`/news/1~20`、`/faq`、`/contact`。

**前置条件**：Django 后端运行在 `127.0.0.1:8000`，系统安装 Chromium。

---

## 七、转化事件埋点

联系表单提交时触发：
- 百度统计：`_hmt.push(['_trackEvent', 'form', 'submit', 'contact_form'])`
- GTM：`dataLayer.push({ event: 'form_submit', form_type: 'contact' })`

后端 `/api/contacts/stats/` 提供线索统计数据。

---

## 八、备案审核通过后收录上线步骤

1. 备案通过，取得 ICP 备案号并填入后台「站点配置」`icp_beian`。
2. 后台「站点配置」填第二节 7+ 项真实验证/统计值。
3. DNS 解析域名到服务器，部署 HTTPS。
4. 重新 `pnpm run build:prerender`（确保快照含最新 TDK 与统计代码）。
5. 各站长平台提交 `sitemap.xml`、验证 meta、开启主动推送。
6. 用 `curl` 抽查预渲染 HTML（含真实正文与 JSON-LD），确认收录就绪。
