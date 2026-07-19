"""
数据库模型定义 - LABOR-SAVING 气动助力机械臂企业官网
核心数据表：用户、资讯、FAQ、表单留言、站点配置
设计原则：字段命名规范、预留扩展字段、适配 Navicat Premium Lite 可视化管理
"""
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """用户表（后台管理员/站点用户）
    继承 Django 自带用户模型，扩展企业相关信息
    """
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系电话')
    avatar = models.CharField(max_length=255, blank=True, null=True, verbose_name='头像')
    department = models.CharField(max_length=50, blank=True, null=True, verbose_name='部门')

    groups = models.ManyToManyField(
        'auth.Group', related_name='api_users', blank=True, verbose_name='用户组'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='api_users', blank=True, verbose_name='用户权限'
    )
    # 预留扩展字段
    ext_field1 = models.CharField(max_length=100, blank=True, null=True, verbose_name='扩展字段1')
    ext_field2 = models.TextField(blank=True, null=True, verbose_name='扩展字段2')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username


class SiteConfig(models.Model):
    """站点配置表 - 全站可配置信息
    存储企业基本信息、SEO全局配置、统计代码等
    """
    site_name = models.CharField(max_length=100, default='LABOR-SAVING 气动助力机械臂', verbose_name='站点名称')
    site_title = models.CharField(max_length=200, default='气动助力机械臂厂家 | 工业机械臂解决方案', verbose_name='站点标题')
    site_keywords = models.CharField(max_length=255, default='气动助力机械臂,助力臂,机械臂厂家,工业自动化', verbose_name='站点关键词')
    site_description = models.TextField(default='LABOR-SAVING 专注气动助力机械臂研发生产，提供工业自动化助力解决方案。', verbose_name='站点描述')

    # 企业实体信息（关于页） - 强化企业信用卡片
    company_name = models.CharField(max_length=100, default='LABOR-SAVING 智能装备有限公司', verbose_name='企业名称')
    company_intro = models.TextField(blank=True, null=True, verbose_name='企业简介')
    founded_year = models.IntegerField(default=2015, verbose_name='成立年份')
    company_scale = models.CharField(max_length=100, blank=True, null=True, verbose_name='经营规模')
    qualifications = models.TextField(blank=True, null=True, verbose_name='资质实力')
    office_address = models.CharField(max_length=200, blank=True, null=True, verbose_name='办公地址')
    service_scope = models.TextField(blank=True, null=True, verbose_name='服务范围')
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系电话')
    contact_email = models.CharField(max_length=100, blank=True, null=True, verbose_name='联系邮箱')
    contact_qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系QQ')

    # 地理位置信息（本地SEO / GEO 结构化数据 - 适配百度地图、Google 地理收录、本地搜索）
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='纬度')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='经度')
    address_region = models.CharField(max_length=50, blank=True, null=True, verbose_name='所在省份')
    address_locality = models.CharField(max_length=50, blank=True, null=True, verbose_name='所在城市/区')
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='邮政编码')

    # SEO 统计与验证代码
    baidu_verify = models.CharField(max_length=100, blank=True, null=True, verbose_name='百度验证代码')
    baidu_tongji = models.CharField(max_length=50, blank=True, null=True, verbose_name='百度统计ID')
    baidu_push_token = models.CharField(max_length=100, blank=True, null=True, verbose_name='百度推送Token')
    qihu_verify = models.CharField(max_length=100, blank=True, null=True, verbose_name='360验证代码')
    qihu_push_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='360自动收录脚本URL')
    sogou_verify = models.CharField(max_length=100, blank=True, null=True, verbose_name='搜狗验证代码')
    google_verify = models.CharField(max_length=100, blank=True, null=True, verbose_name='Google验证代码')
    google_ga_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='Google Analytics ID')
    google_ads_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='Google Ads ID')
    gtm_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='GTM容器ID')

    # ICP 备案信息（备案通过后填入 SiteConfig.icp_beian，前端页脚展示；管局审核中先留空）
    icp_beian = models.CharField(max_length=50, blank=True, null=True, verbose_name='ICP备案号')
    icp_link = models.CharField(max_length=200, blank=True, null=True,
                                default='https://beian.miit.gov.cn', verbose_name='备案查询链接')

    # 预留扩展字段
    ext_config1 = models.TextField(blank=True, null=True, verbose_name='扩展配置1')
    ext_config2 = models.TextField(blank=True, null=True, verbose_name='扩展配置2')

    class Meta:
        db_table = 'site_config'
        verbose_name = '站点配置'
        verbose_name_plural = '站点配置'

    def __str__(self):
        return self.site_name


class Article(models.Model):
    """资讯/博客文章表"""
    STATUS_CHOICES = (
        (1, '已发布'),
        (0, '已下架'),
    )

    title = models.CharField(max_length=200, verbose_name='文章标题')
    # 独立 SEO TDK
    seo_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='SEO标题')
    seo_keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name='SEO关键词')
    seo_description = models.TextField(blank=True, null=True, verbose_name='SEO描述')

    category = models.CharField(max_length=50, default='行业资讯', verbose_name='文章分类')
    # URL 别名（语义化 SEO 友好链接，如 /news/qizhong-xitong，默认空则回退数字 ID）
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True, verbose_name='URL别名')
    cover = models.CharField(max_length=255, blank=True, null=True, verbose_name='封面图URL')
    # 封面图（关联媒体库上传文件，优先于 cover 字段）
    cover_image = models.ForeignKey('Media', on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='article_covers', verbose_name='封面图(媒体库)')
    summary = models.TextField(blank=True, null=True, verbose_name='文章摘要')
    # 文章内容（支持 HTML 富文本，后台可排版图文）
    content = models.TextField(verbose_name='文章内容')
    author = models.CharField(max_length=50, default='管理员', verbose_name='作者')
    views = models.IntegerField(default=0, verbose_name='浏览量')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 预留扩展字段
    ext_field1 = models.CharField(max_length=100, blank=True, null=True, verbose_name='扩展字段1')
    ext_field2 = models.TextField(blank=True, null=True, verbose_name='扩展字段2')

    class Meta:
        db_table = 'article'
        verbose_name = '资讯文章'
        verbose_name_plural = '资讯文章'
        ordering = ['-is_top', '-sort_order', '-created_at']

    def __str__(self):
        return self.title


class Faq(models.Model):
    """FAQ 采购高频问答表
    固定结构：问题 → 2-3句答案 → 详细展开说明
    """
    question = models.CharField(max_length=255, verbose_name='问题')
    answer = models.TextField(verbose_name='精简答案（2-3句）')
    detail = models.TextField(blank=True, null=True, verbose_name='详细展开说明')
    category = models.CharField(max_length=50, default='通用', verbose_name='分类')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否显示')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 预留扩展字段
    ext_field1 = models.CharField(max_length=100, blank=True, null=True, verbose_name='扩展字段1')

    class Meta:
        db_table = 'faq'
        verbose_name = 'FAQ问答'
        verbose_name_plural = 'FAQ问答'
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return self.question


class Contact(models.Model):
    """联系表单/线索留言表"""
    name = models.CharField(max_length=50, verbose_name='姓名')
    phone = models.CharField(max_length=20, verbose_name='电话')
    email = models.CharField(max_length=100, blank=True, null=True, verbose_name='邮箱')
    message = models.TextField(verbose_name='留言内容')
    source = models.CharField(max_length=50, blank=True, null=True, verbose_name='来源页面')
    ip_address = models.CharField(max_length=50, blank=True, null=True, verbose_name='IP地址')
    is_handled = models.BooleanField(default=False, verbose_name='是否已处理')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')

    # 预留扩展字段
    ext_field1 = models.CharField(max_length=100, blank=True, null=True, verbose_name='扩展字段1')

    class Meta:
        db_table = 'contact'
        verbose_name = '联系表单'
        verbose_name_plural = '联系表单'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.phone}'


class Product(models.Model):
    """产品表 - 企业核心产品/服务，后台可配置"""
    name = models.CharField(max_length=100, verbose_name='产品名称')
    icon = models.CharField(max_length=10, default='🔧', verbose_name='显示图标')
    description = models.TextField(verbose_name='产品描述')
    category = models.CharField(max_length=50, default='核心产品', verbose_name='产品分类')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否显示')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 预留扩展字段
    ext_field1 = models.CharField(max_length=100, blank=True, null=True, verbose_name='扩展字段1')

    class Meta:
        db_table = 'product'
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return self.name


class Certificate(models.Model):
    """资质证书表 - 后台可上传、排序展示"""
    name = models.CharField(max_length=100, verbose_name='证书名称')
    image_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='证书图片URL')
    # 证书图片（关联媒体库上传文件，优先于 image_url 字段）
    image = models.ForeignKey('Media', on_delete=models.SET_NULL, blank=True, null=True,
                              related_name='certificates', verbose_name='证书图片(媒体库)')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='证书说明')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否显示')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'certificate'
        verbose_name = '资质证书'
        verbose_name_plural = '资质证书'
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return self.name


class Milestone(models.Model):
    """企业历程时间线表 - 后台可配置"""
    year = models.CharField(max_length=20, verbose_name='年份')
    title = models.CharField(max_length=200, verbose_name='里程碑事件')
    description = models.TextField(blank=True, null=True, verbose_name='详细描述')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否显示')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'milestone'
        verbose_name = '企业历程'
        verbose_name_plural = '企业历程'
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f'{self.year} - {self.title}'


class ArticleLike(models.Model):
    """文章点赞记录表"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes', verbose_name='文章')
    ip_address = models.CharField(max_length=50, blank=True, null=True, verbose_name='IP地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        db_table = 'article_like'
        verbose_name = '文章点赞'
        verbose_name_plural = '文章点赞'

    def __str__(self):
        return f'{self.article_id} - {self.ip_address}'


class Media(models.Model):
    """媒体图库 - 图片/文档/视频统一上传与管理
    采用 FileField（不依赖 Pillow），覆盖产品实拍图、证书扫描件、参数册 PDF、车间视频等
    """
    MEDIA_TYPE_CHOICES = (
        ('image', '图片'),
        ('document', '文档'),
        ('video', '视频'),
    )

    title = models.CharField(max_length=200, verbose_name='文件标题')
    file = models.FileField(upload_to='uploads/%Y/%m/', verbose_name='文件')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default='image', verbose_name='媒体类型')
    file_size = models.IntegerField(default=0, verbose_name='文件大小(字节)')
    mime_type = models.CharField(max_length=100, blank=True, null=True, verbose_name='MIME类型')
    uploaded_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='上传者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    # 预留扩展字段
    ext_field1 = models.CharField(max_length=100, blank=True, null=True, verbose_name='扩展字段1')

    class Meta:
        db_table = 'media'
        verbose_name = '媒体文件'
        verbose_name_plural = '媒体图库'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def url(self):
        """对外访问地址（MEDIA_URL + 相对路径）"""
        return settings.MEDIA_URL + self.file.name


class LoginLog(models.Model):
    """登录日志 - 安全审计（记录后台登录/登出/失败事件）"""
    ACTION_CHOICES = (
        ('login', '登录成功'),
        ('logout', '退出登录'),
        ('failed', '登录失败'),
    )

    username = models.CharField(max_length=150, verbose_name='用户名')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='关联用户')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='动作')
    ip_address = models.CharField(max_length=50, blank=True, null=True, verbose_name='IP地址')
    user_agent = models.TextField(blank=True, null=True, verbose_name='浏览器标识')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        db_table = 'login_log'
        verbose_name = '登录日志'
        verbose_name_plural = '登录日志'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.username} - {self.get_action_display()} - {self.ip_address}'


class ApiKey(models.Model):
    """API 密钥管理 - 对外接口授权（自研 Token，无第三方依赖）"""
    SCOPE_CHOICES = (
        ('read', '只读'),
        ('write', '读写'),
        ('admin', '管理'),
    )

    name = models.CharField(max_length=100, verbose_name='密钥名称')
    key_prefix = models.CharField(max_length=12, verbose_name='密钥前缀')
    key_hash = models.CharField(max_length=128, verbose_name='密钥哈希')
    scopes = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='read', verbose_name='权限范围')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    last_used_at = models.DateTimeField(blank=True, null=True, verbose_name='最后使用时间')
    created_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 预留扩展字段
    ext_field1 = models.CharField(max_length=100, blank=True, null=True, verbose_name='扩展字段1')

    class Meta:
        db_table = 'api_key'
        verbose_name = 'API密钥'
        verbose_name_plural = 'API密钥管理'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.key_prefix}••••)'


class IpRule(models.Model):
    """IP 规则 - 黑白名单管理（防护后台爆破/接口滥用）"""
    RULE_TYPE_CHOICES = (
        ('allow', '白名单'),
        ('deny', '黑名单'),
    )
    SCOPE_CHOICES = (
        ('all', '全站'),
        ('admin', '后台管理'),
        ('api', 'API接口'),
    )

    ip_address = models.CharField(max_length=50, verbose_name='IP地址/CIDR')
    rule_type = models.CharField(max_length=10, choices=RULE_TYPE_CHOICES, default='deny', verbose_name='规则类型')
    scope = models.CharField(max_length=10, choices=SCOPE_CHOICES, default='all', verbose_name='生效范围')
    note = models.CharField(max_length=200, blank=True, null=True, verbose_name='备注')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'ip_rule'
        verbose_name = 'IP规则'
        verbose_name_plural = 'IP黑白名单'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_rule_type_display()} {self.ip_address} ({self.get_scope_display()})'
