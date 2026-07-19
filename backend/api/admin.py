"""
Django Admin 后台管理配置
实现数据可视化增删改查，支持 FAQ、资讯、表单等后台管理
定制国际化面板、操作日志记录
"""
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponse
from django.urls import path
from django.utils.safestring import mark_safe
from .models import (Article, Faq, Contact, SiteConfig, Product, Certificate,
                     Milestone, ArticleLike, Media, LoginLog, ApiKey, IpRule)


class BaseAdminMixin:
    """统一管理面板配置"""
    list_per_page = 20
    save_on_top = True


@admin.register(SiteConfig)
class SiteConfigAdmin(BaseAdminMixin, admin.ModelAdmin):
    """站点配置管理"""
    list_display = ['site_name', 'company_name', 'founded_year']
    fieldsets = (
        ('基础信息', {'fields': ('site_name', 'site_title', 'site_keywords', 'site_description')}),
        ('企业实体信息', {'fields': ('company_name', 'company_intro', 'founded_year',
                                    'company_scale', 'qualifications', 'office_address',
                                    'address_region', 'address_locality', 'postal_code',
                                    'latitude', 'longitude',
                                    'service_scope', 'contact_phone', 'contact_email', 'contact_qq')}),
        ('SEO 统计验证', {'fields': ('baidu_verify', 'baidu_tongji', 'baidu_push_token',
                                    'qihu_verify', 'sogou_verify', 'google_verify',
                                    'google_ga_id', 'google_ads_id', 'gtm_id')}),
    )


@admin.register(Article)
class ArticleAdmin(BaseAdminMixin, admin.ModelAdmin):
    """资讯文章管理"""
    list_display = ['title', 'slug', 'category', 'author', 'views', 'like_count', 'status', 'is_top', 'sort_order', 'created_at']
    list_filter = ['category', 'status', 'is_top']
    search_fields = ['title', 'content', 'slug']
    list_editable = ['status', 'is_top', 'sort_order']
    readonly_fields = ['views', 'created_at', 'updated_at', 'like_count']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('基础信息', {'fields': ('title', 'slug', 'category', 'author', 'status', 'is_top', 'sort_order')}),
        ('SEO TDK', {'fields': ('seo_title', 'seo_keywords', 'seo_description'), 'classes': ('collapse',)}),
        ('内容', {'fields': ('summary', 'content')}),
        ('封面', {'fields': ('cover', 'cover_image')}),
    )

    def like_count(self, obj):
        return ArticleLike.objects.filter(article=obj).count()
    like_count.short_description = '点赞数'

    class Media:
        js = ('api/richtext.js',)
        css = {'all': ('api/richtext.css',)}


@admin.register(Faq)
class FaqAdmin(BaseAdminMixin, admin.ModelAdmin):
    """FAQ 问答管理"""
    list_display = ['question', 'category', 'is_active', 'sort_order', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    list_editable = ['is_active', 'sort_order']


@admin.register(Contact)
class ContactAdmin(BaseAdminMixin, admin.ModelAdmin):
    """联系表单管理"""
    list_display = ['name', 'phone', 'source', 'is_handled', 'created_at']
    list_filter = ['is_handled', 'source']
    search_fields = ['name', 'phone', 'message']
    readonly_fields = ['name', 'phone', 'email', 'message', 'source', 'ip_address', 'created_at']
    list_editable = ['is_handled']
    actions = ['export_csv']

    def export_csv(self, request, queryset):
        """CSV 导出"""
        import csv
        from django.utils.timezone import localtime
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="contacts_export.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', '姓名', '电话', '邮箱', '留言', '来源', 'IP', '已处理', '提交时间'])
        for c in queryset:
            writer.writerow([
                c.id, c.name, c.phone, c.email, c.message, c.source,
                c.ip_address, '是' if c.is_handled else '否',
                localtime(c.created_at).strftime('%Y-%m-%d %H:%M') if c.created_at else ''
            ])
        return response
    export_csv.short_description = '导出选中数据为 CSV'


@admin.register(Product)
class ProductAdmin(BaseAdminMixin, admin.ModelAdmin):
    """产品管理"""
    list_display = ['name', 'category', 'sort_order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['sort_order', 'is_active']


@admin.register(Certificate)
class CertificateAdmin(BaseAdminMixin, admin.ModelAdmin):
    """资质证书管理"""
    list_display = ['name', 'image', 'sort_order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['sort_order', 'is_active']


@admin.register(Milestone)
class MilestoneAdmin(BaseAdminMixin, admin.ModelAdmin):
    """企业历程管理"""
    list_display = ['year', 'title', 'sort_order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['sort_order', 'is_active']


@admin.register(ArticleLike)
class ArticleLikeAdmin(BaseAdminMixin, admin.ModelAdmin):
    """文章点赞管理"""
    list_display = ['article', 'ip_address', 'created_at']
    readonly_fields = ['article', 'ip_address', 'created_at']
    list_filter = ['created_at']


# 自定义 Admin 站点标题
admin.site.site_header = 'LABOR-SAVING 企业官网管理后台'
admin.site.site_title = 'LABOR-SAVING 后台管理'
admin.site.index_title = '欢迎使用企业官网管理系统'


@admin.register(Media)
class MediaAdmin(BaseAdminMixin, admin.ModelAdmin):
    """媒体图库管理 - 后台上传图片/文档/视频"""
    list_display = ['title', 'media_type', 'file_size', 'uploaded_by', 'created_at']
    list_filter = ['media_type']
    search_fields = ['title']
    readonly_fields = ['file_size', 'mime_type', 'created_at']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 保存后回填文件大小与 MIME 类型
        if obj.file:
            obj.file_size = obj.file.size
            obj.mime_type = getattr(obj.file, 'content_type', '') or ''
            obj.save(update_fields=['file_size', 'mime_type'])


@admin.register(LoginLog)
class LoginLogAdmin(BaseAdminMixin, admin.ModelAdmin):
    """登录日志管理 - 安全审计"""
    list_display = ['username', 'action', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['username', 'ip_address']
    readonly_fields = ['username', 'user', 'action', 'ip_address', 'user_agent', 'created_at']
    list_per_page = 30

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ApiKey)
class ApiKeyAdmin(BaseAdminMixin, admin.ModelAdmin):
    """API 密钥管理 - 创建时生成密钥明文（仅展示一次）"""
    list_display = ['name', 'key_prefix', 'scopes', 'is_active', 'last_used_at', 'created_at']
    list_filter = ['scopes', 'is_active']
    search_fields = ['name', 'key_prefix']
    readonly_fields = ['key_prefix', 'key_hash', 'last_used_at', 'created_at']
    actions = ['disable_selected', 'enable_selected']

    @admin.action(description='停用选中密钥')
    def disable_selected(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description='启用选中密钥')
    def enable_selected(self, request, queryset):
        queryset.update(is_active=True)

    def save_model(self, request, obj, form, change):
        if not change and not obj.key_hash:
            from api.auth import generate_api_key
            plain, prefix, key_hash = generate_api_key()
            obj.key_prefix = prefix
            obj.key_hash = key_hash
            obj.created_by = request.user.username if request.user.is_authenticated else 'admin'
            super().save_model(request, obj, form, change)
            self.message_user(
                request,
                f'密钥已创建，明文（请立即复制保存，后续不可见）：{plain}',
                level=messages.SUCCESS
            )
        else:
            super().save_model(request, obj, form, change)


@admin.register(IpRule)
class IpRuleAdmin(BaseAdminMixin, admin.ModelAdmin):
    """IP 黑白名单管理"""
    list_display = ['ip_address', 'rule_type', 'scope', 'is_active', 'note', 'created_at']
    list_filter = ['rule_type', 'scope', 'is_active']
    search_fields = ['ip_address', 'note']
    list_editable = ['is_active']
    actions = ['disable_selected', 'enable_selected']

    @admin.action(description='停用选中规则')
    def disable_selected(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description='启用选中规则')
    def enable_selected(self, request, queryset):
        queryset.update(is_active=True)
