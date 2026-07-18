# Navicat Premium Lite 数据库配置教程

本文档指导使用 Navicat Premium Lite 管理本项目 SQLite 数据库。

---

## 一、连接数据库

1. 打开 Navicat Premium Lite，点击左上角 **「连接」** → 选择 **「SQLite」**
2. 连接名称：填写 `laborsaving_arm`（自定义）
3. 数据库文件：选择项目路径 `backend/db.sqlite3`
4. 点击 **「测试连接」** → 显示「连接成功」→ **「确定」**

> 注：db.sqlite3 由 Django 迁移自动生成，首次运行 `python manage.py migrate` 后产生

---

## 二、表结构查看与管理

连接成功后，展开连接 → 数据库 → 表，可见以下核心表：

| 表名 | 说明 | 关键字段 |
|------|------|----------|
| `user` | 用户表 | username, phone, department |
| `site_config` | 站点配置 | site_name, company_name, baidu_verify... |
| `article` | 资讯文章 | title, content, seo_title, views, status |
| `faq` | FAQ问答 | question, answer, detail, category |
| `contact` | 联系表单 | name, phone, message, is_handled |

---

## 三、数据增删改查（可视化操作）

### 新增 FAQ
1. 双击打开 `faq` 表 → 点击 **「+」** 或 **「新建记录」**
2. 填写字段：
   - `question`：问题内容
   - `answer`：精简答案（2-3句）
   - `detail`：详细展开说明
   - `category`：分类（如「产品认知」「选型对比」）
   - `sort_order`：排序序号
   - `is_active`：是否显示（1显示/0隐藏）
3. **「Ctrl+S」** 保存

### 编辑资讯文章
1. 双击 `article` 表 → 找到目标行双击进入编辑
2. 修改 `title`、`content`、`seo_title` 等字段
3. 修改 `status`（1发布/0下架）控制上下架
4. 保存

### 查看表单线索
1. 双击 `contact` 表 → 查看用户提交的姓名、电话、留言
2. 处理后将 `is_handled` 改为 1 标记已处理

---

## 四、数据备份与导出

### 导出备份
1. 右键点击数据库 → **「转储SQL文件」** → **「结构和数据」**
2. 选择保存路径，生成 `.sql` 备份文件

### 导出单表数据
1. 右键点击表 → **「导出向导」**
2. 选择格式（JSON / Excel / CSV）→ 按向导完成

### 导入数据
1. 右键点击表 → **「导入向导」**
2. 选择源文件格式 → 映射字段 → 完成导入

---

## 五、注意事项

- ⚠️ 修改 `site_config` 表时确保只有一条记录（id=1）
- ⚠️ 生产环境备份请定期执行「转储SQL文件」
- ⚠️ 字段命名已规范化，请勿随意修改字段名
- ⚠️ 预留 `ext_field1`、`ext_field2` 等扩展字段，可自由使用

---

## 六、常见问题

**Q：连接报错「unable to open database file」？**
A：确认 db.sqlite3 已生成（运行过 migrate），且路径正确。

**Q：修改数据后前台不显示？**
A：检查 `status`/`is_active` 是否为启用状态，刷新前台页面。

**Q：如何重置数据库？**
A：删除 db.sqlite3，重新执行 `python manage.py migrate` 和初始化脚本。
