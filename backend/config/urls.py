"""URL 路由配置 - LABOR-SAVING 企业官网后端"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # API 接口路由前缀
    path('api/', include('api.urls')),
    # SEO 相关路由（llms.txt、sitemap等）
    path('', include('api.seo_urls')),
]
