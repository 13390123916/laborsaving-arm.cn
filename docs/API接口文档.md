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
```
> 访问时浏览量自动 +1

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

## 五、SEO 路由

| 路径 | 说明 |
|------|------|
| `/llms.txt` | AI 引擎友好索引文件 |
| `/robots.txt` | 爬虫规则 |
| `/sitemap.xml` | 站点地图 |
| `/schema/organization.json` | 企业结构化数据 |

---

## 六、错误码

| code | 说明 |
|------|------|
| 200 | 成功 |
| 400 | 参数错误 / 提交失败 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |
