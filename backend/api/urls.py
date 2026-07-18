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
    path('articles/<int:pk>/', views.ArticleViewSet.as_view({'get': 'retrieve'}), name='article-detail'),
    # FAQ
    path('faqs/', views.FaqViewSet.as_view({'get': 'list'}), name='faq-list'),
    # 联系表单
    path('contacts/', views.ContactViewSet.as_view({'post': 'create'}), name='contact-create'),
    path('contacts/stats/', views.ContactViewSet.as_view({'get': 'stats'}), name='contact-stats'),
]
