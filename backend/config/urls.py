"""URL 路由配置 - LABOR-SAVING 企业官网后端"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse, Http404
from django.views.static import serve
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    # API 接口路由前缀
    path('api/', include('api.urls')),
    # SEO 相关路由（llms.txt、sitemap、schema 等）
    path('', include('api.seo_urls')),
]

# 开发环境（DEBUG）直接由 Django 提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ===== 生产环境 SPA 兜底 =====
# 当 SERVE_SPA=True 时，将未匹配的路径指向 Vue 构建产物
# 优先按路由返回预渲染快照（dist/<route>/index.html），
# 兜底返回 dist/index.html（SPA 入口），确保爬虫拿到正确 TDK 与内容
if getattr(settings, 'SERVE_SPA', False):
    dist_dir = getattr(settings, 'FRONTEND_DIST_DIR', None)

    def spa_fallback(request, **kwargs):
        """按路由优先返回预渲染快照，兜底返回 SPA 入口"""
        if not dist_dir:
            return HttpResponse('SPA not built. Run `pnpm build` in frontend/.', status=503)

        path = request.path.lstrip('/')
        dist_str = str(dist_dir)

        # 1) 优先返回按路由预渲染快照：dist/<path>/index.html
        #    例如 /about → dist/about/index.html
        #         /news/5 → dist/news/5/index.html
        if path:
            cand = os.path.join(dist_str, path, 'index.html')
            if os.path.exists(cand):
                with open(cand, 'r', encoding='utf-8') as f:
                    return HttpResponse(f.read())

        # 2) 兜底返回 SPA 入口 dist/index.html（含预渲染首页或空壳）
        index_path = os.path.join(dist_str, 'index.html')
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                return HttpResponse(f.read())

        return HttpResponse('SPA not built. Run `pnpm build` in frontend/.', status=503)

    urlpatterns += [
        # 媒体文件（上传的图片/文档/视频）由 Django 提供静态服务
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media-serve'),
        # 静态资产 /assets/、/static/ 由 Django 自动服务（STATICFILES_DIRS 已指向 dist）
        # 所有非 /api、/admin、/static、/media、/assets 路径 → 按路由快照分发
        # 注意：必须排除 /assets/，否则 JS/CSS 会被兜底成 index.html（HTML），导致前端交互失效
        re_path(r'^(?!api/|admin/|static/|media/|assets/|favicon\.ico).*$', spa_fallback, name='spa-fallback'),
    ]
