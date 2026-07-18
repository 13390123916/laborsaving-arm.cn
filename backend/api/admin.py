"""
Django Admin 后台管理配置
实现数据可视化增删改查，支持 FAQ、资讯、表单等后台管理
"""
from django.contrib import admin
from .models import Article, Faq, Contact, SiteConfig, Product


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    """站点配置管理"""
    list_display = ['site_name', 'company_name', 'founded_year']
    fieldsets = (
        ('基础信息', {'fields': ('site_name', 'site_title', 'site_keywords', 'site_description')}),
        ('企业实体信息', {'fields': ('company_name', 'company_intro', 'founded_year',
                                    'company_scale', 'qualifications', 'office_address',
                                    'service_scope', 'contact_phone', 'contact_email', 'contact_qq')}),
        ('SEO 统计验证', {'fields': ('baidu_verify', 'baidu_tongji', 'baidu_push_token',
                                    'qihu_verify', 'sogou_verify', 'google_verify',
                                    'google_ga_id', 'google_ads_id', 'gtm_id')}),
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """资讯文章管理"""
    list_display = ['title', 'category', 'author', 'views', 'status', 'is_top', 'sort_order', 'created_at']
    list_filter = ['category', 'status', 'is_top']
    search_fields = ['title', 'content']
    list_editable = ['status', 'is_top', 'sort_order']
    readonly_fields = ['views', 'created_at', 'updated_at']


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    """FAQ 问答管理"""
    list_display = ['question', 'category', 'is_active', 'sort_order', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    list_editable = ['is_active', 'sort_order']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """联系表单管理"""
    list_display = ['name', 'phone', 'source', 'is_handled', 'created_at']
    list_filter = ['is_handled', 'source']
    search_fields = ['name', 'phone', 'message']
    readonly_fields = ['name', 'phone', 'email', 'message', 'source', 'ip_address', 'created_at']
    list_editable = ['is_handled']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """产品管理"""
    list_display = ['name', 'category', 'sort_order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['sort_order', 'is_active']
