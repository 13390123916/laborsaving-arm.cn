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

### 1. Organization Schema
访问 `/schema/organization.json` 获取企业结构化数据（JSON-LD），包含：
- 企业名称、描述、成立时间
- 地址、联系方式
- 适配搜索引擎结构化展示与 AI 摘要抓取

### 2. FAQ Schema（页面内）
FAQ 页面采用标准问答结构，建议前端在页面注入 FAQPage 类型的 JSON-LD（后续可扩展）

### 3. Article Schema（文章详情页）
建议文章详情页注入 `Article` 类型结构化数据，包含标题、作者、发布时间

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

## 五、转化事件埋点

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
