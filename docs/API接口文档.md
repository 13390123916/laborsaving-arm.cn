# API 接口文档 - LABOR-SAVING 企业官网

基础地址：`http://域名/api/`
统一返回格式：
```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

---

## 一、站点配置

### 获取站点配置
```
GET /api/site-config/info/
```
**响应示例：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "site_name": "LABOR-SAVING 气动助力机械臂",
    "company_name": "LABOR-SAVING 智能装备有限公司",
    "founded_year": 2015,
    "baidu_verify": "xxx",
    "baidu_tongji": "xxxxxx"
  }
}
```

---

## 二、资讯文章

### 文章列表
```
GET /api/articles/?page=1&page_size=10&category=行业资讯
```
**参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码，默认1 |
| page_size | int | 每页数量，默认10 |
| category | string | 分类筛选（可选） |

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      { "id": 1, "title": "...", "category": "...", "cover": "...", "summary": "...", "views": 0 }
    ],
    "total": 3,
    "page": 1,
    "page_size": 10
  }
}
```

### 文章详情
```
GET /api/articles/{id}/
GET /api/articles/{slug}/        # 支持语义化 URL 别名（slug），未设置 slug 时回退数字 ID
```
> 访问时浏览量自动 +1；列表与详情均返回 `cover_image_url`（媒体库封面，优先于旧 `cover` 字段）。
> 文章内容支持富文本 HTML（含图文混排），前端以 `v-html` 渲染。

### 文章分类列表
```
GET /api/articles/categories/
```
**响应：** `["公司新闻", "行业资讯", "技术干货"]`

---

## 三、FAQ 问答

### FAQ 列表
```
GET /api/faqs/?category=产品认知
```
**参数：** category（可选，按分类筛选）

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    { "id": 1, "question": "...", "answer": "...", "detail": "...", "category": "..." }
  ]
}
```

---

## 四、联系表单

### 提交表单
```
POST /api/contacts/
```
**请求体：**
```json
{
  "name": "张三",
  "phone": "13800138000",
  "email": "zhangsan@email.com",
  "message": "咨询500kg机械臂报价"
}
```
**响应：**
```json
{
  "code": 200,
  "message": "提交成功，我们会尽快与您联系",
  "data": { "id": 1, "name": "张三", "phone": "13800138000" }
}
```

### 表单统计
```
GET /api/contacts/stats/
```
**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": { "total": 10, "handled": 3, "pending": 7 }
}
```

---

## 五、产品

### 产品列表
```
GET /api/products/
```
**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    { "id": 1, "name": "气动助力机械臂", "icon": "🦾", "description": "..." }
  ]
}
```

---

## 六、SEO 路由

| 路径 | 说明 |
|------|------|
| `/llms.txt` | AI 引擎友好索引文件 |
| `/robots.txt` | 爬虫规则 |
| `/sitemap.xml` | 站点地图 |

---

## 七、媒体图库接口

| 路径 | 方法 | 权限 | 说明 |
|------|------|------|------|
| `/api/media/` | GET | 公开 | 媒体列表（可按 `?type=image` 筛选） |
| `/api/media/` | POST | API 密钥（write/admin） | 上传文件（multipart：`file`、`title`、`uploaded_by`） |
| `/api/media/{id}/` | DELETE | API 密钥（admin） | 删除媒体及物理文件 |

**上传响应示例：**
```json
{ "code": 200, "message": "上传成功",
  "data": { "id": 1, "title": "产品实拍", "url": "/media/uploads/2026/07/xxx.jpg", "media_type": "image" } }
```

---

## 八、安全与审计接口（需 admin 密钥）

| 路径 | 方法 | 说明 |
|------|------|------|
| `/api/login-logs/` | GET | 登录审计日志（支持 `?action=login\|logout\|failed` 筛选、分页） |
| `/api/ip-rules/` | GET | IP 黑白名单列表 |
| `/api/ip-rules/` | POST | 新增规则（`ip_address`、`rule_type=allow\|deny`、`scope=all\|admin\|api`、`note`） |
| `/api/ip-rules/{id}/` | DELETE / PATCH | 删除 / 启用停用规则 |

> 后台 `/admin/` 登录失败 5 次/15 分钟将自动临时锁定该 IP；IP 黑名单命中即拦截，白名单模式下仅放行列表内 IP。

---

## 九、API 密钥管理接口（需 admin 密钥）

| 路径 | 方法 | 说明 |
|------|------|------|
| `/api/api-keys/` | GET | 密钥列表（不含明文与哈希） |
| `/api/api-keys/` | POST | 创建密钥（`name`、`scopes=read\|write\|admin`），返回一次性明文 `plain_key` |
| `/api/api-keys/{id}/` | DELETE / PATCH | 删除 / 启用停用密钥 |

**密钥使用方式（自研 Token，无第三方依赖）：**
```
Authorization: Bearer <prefix>.<secret>
# 或查询参数兜底：?api_key=<prefix>.<secret>
```
> 首个密钥请在 Django Admin「API密钥管理」中创建（明文仅显示一次）；后续可在 Admin 或通过上述接口管理。

---

## 十、错误码

| code | 说明 |
|------|------|
| 200 | 成功 |
| 400 | 参数错误 / 提交失败 |
| 401 / 403 | 未携带有效 API 密钥 / 权限不足 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁（表单/点赞接口限流） |
| 500 | 服务器错误 |
