"""
URL 路由 - API 接口
统一前缀 /api/
"""
from django.urls import path
from . import views

urlpatterns = [
    # 站点配置
    path('site-config/info/', views.SiteConfigViewSet.as_view({'get': 'info'}), name='site-config-info'),
    # 资讯文章
    path('articles/', views.ArticleViewSet.as_view({'get': 'list'}), name='article-list'),
    path('articles/categories/', views.ArticleViewSet.as_view({'get': 'categories'}), name='article-categories'),
    path('articles/<path:pk>/', views.ArticleViewSet.as_view({'get': 'retrieve'}), name='article-detail'),
    # FAQ
    path('faqs/', views.FaqViewSet.as_view({'get': 'list'}), name='faq-list'),
    # 联系表单
    path('contacts/', views.ContactViewSet.as_view({'post': 'create'}), name='contact-create'),
    path('contacts/stats/', views.ContactViewSet.as_view({'get': 'stats'}), name='contact-stats'),
    # 产品
    path('products/', views.ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    # 资质证书
    path('certificates/', views.CertificateViewSet.as_view({'get': 'list'}), name='certificate-list'),
    # 企业历程
    path('milestones/', views.MilestoneViewSet.as_view({'get': 'list'}), name='milestone-list'),
    # 文章点赞
    path('article-likes/', views.ArticleLikeViewSet.as_view({'post': 'create'}), name='article-like-create'),
    path('article-likes/count/', views.ArticleLikeViewSet.as_view({'get': 'count'}), name='article-like-count'),
    # 媒体图库
    path('media/', views.MediaViewSet.as_view({'get': 'list', 'post': 'upload'}), name='media-list'),
    path('media/<int:pk>/', views.MediaViewSet.as_view({'delete': 'remove'}), name='media-detail'),
    # 登录日志（需 admin 密钥）
    path('login-logs/', views.LoginLogViewSet.as_view({'get': 'list'}), name='login-logs'),
    # API 密钥管理（需 admin 密钥）
    path('api-keys/', views.ApiKeyViewSet.as_view({'get': 'list', 'post': 'create'}), name='apikey-list'),
    path('api-keys/<int:pk>/', views.ApiKeyViewSet.as_view({'delete': 'remove', 'patch': 'disable'}), name='apikey-detail'),
    # IP 黑白名单（需 admin 密钥）
    path('ip-rules/', views.IpRuleViewSet.as_view({'get': 'list', 'post': 'create'}), name='iprule-list'),
    path('ip-rules/<int:pk>/', views.IpRuleViewSet.as_view({'delete': 'remove', 'patch': 'disable'}), name='iprule-detail'),
]
