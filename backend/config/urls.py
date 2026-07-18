"""URL 路由配置 - LABOR-SAVING 企业官网后端"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponse
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    # API 接口路由前缀
    path('api/', include('api.urls')),
    # SEO 相关路由（llms.txt、sitemap、schema 等）
    path('', include('api.seo_urls')),
]

# ===== 生产环境 SPA 兜底 =====
# 当 SERVE_SPA=True 时，将未匹配的路径指向 Vue 构建产物 index.html
# 确保 /news/5、/faq、/contact 等 SPA 路由在后端直接可访问
if getattr(settings, 'SERVE_SPA', False):
    dist_dir = getattr(settings, 'FRONTEND_DIST_DIR', None)
    index_path = os.path.join(str(dist_dir), 'index.html') if dist_dir else None

    def spa_fallback(request, **kwargs):
        """读取 dist/index.html 作为 SPA 入口"""
        if index_path and os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                return HttpResponse(f.read())
        return HttpResponse('SPA not built. Run `pnpm build` in frontend/.', status=503)

    urlpatterns += [
        # 静态资产 /assets/ 由 Django 自动服务（STATICFILES_DIRS 已指向 dist）
        # 所有非 /api、/admin、/static 路径 → 返回 index.html
        re_path(r'^(?!api/|admin/|static/|media/).*$', spa_fallback, name='spa-fallback'),
    ]
