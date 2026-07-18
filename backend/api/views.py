"""
视图函数 - RESTful API 接口
所有接口统一返回格式：{code, message, data}
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Article, Faq, Contact, SiteConfig, Product
from .serializers import (SiteConfigSerializer, ArticleListSerializer,
                          ArticleDetailSerializer, FaqSerializer, ContactSerializer,
                          ProductSerializer)


class SiteConfigViewSet(viewsets.ViewSet):
    """站点配置接口"""
    @action(detail=False, methods=['get'])
    def info(self, request):
        """获取站点配置"""
        config = SiteConfig.objects.first()
        if not config:
            # 首次访问自动创建默认配置
            config = SiteConfig.objects.create()
        return Response({
            'code': 200,
            'message': 'success',
            'data': SiteConfigSerializer(config).data
        })


class ArticleViewSet(viewsets.ViewSet):
    """资讯文章接口"""
    def list(self, request):
        """文章列表（支持分类筛选）"""
        queryset = Article.objects.filter(status=1)
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        items = queryset[start:end]
        return Response({
            'code': 200,
            'message': 'success',
            'data': {
                'list': ArticleListSerializer(items, many=True).data,
                'total': total,
                'page': page,
                'page_size': page_size
            }
        })

    def retrieve(self, request, pk=None):
        """文章详情（浏览量+1）"""
        try:
            article = Article.objects.get(id=pk, status=1)
        except Article.DoesNotExist:
            return Response({'code': 404, 'message': '文章不存在', 'data': None},
                            status=status.HTTP_404_NOT_FOUND)
        # 浏览量自增
        article.views += 1
        article.save()
        return Response({
            'code': 200,
            'message': 'success',
            'data': ArticleDetailSerializer(article).data
        })

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """获取文章分类列表"""
        cats = Article.objects.filter(status=1).values_list('category', flat=True).distinct()
        return Response({
            'code': 200,
            'message': 'success',
            'data': list(cats)
        })


class FaqViewSet(viewsets.ViewSet):
    """FAQ问答接口"""
    def list(self, request):
        """FAQ列表（支持分类筛选）"""
        queryset = Faq.objects.filter(is_active=True)
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return Response({
            'code': 200,
            'message': 'success',
            'data': FaqSerializer(queryset, many=True).data
        })


@method_decorator(csrf_exempt, name='create')
class ContactViewSet(viewsets.ViewSet):
    """联系表单接口"""
    def create(self, request):
        """提交表单留言"""
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            # 获取客户端IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            serializer.save(ip_address=ip)
            return Response({
                'code': 200,
                'message': '提交成功，我们会尽快与您联系',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': 400,
            'message': '提交失败',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """表单统计（线索数）"""
        total = Contact.objects.count()
        handled = Contact.objects.filter(is_handled=True).count()
        return Response({
            'code': 200,
            'message': 'success',
            'data': {
                'total': total,
                'handled': handled,
                'pending': total - handled
            }
        })


class ProductViewSet(viewsets.ViewSet):
    """产品接口"""
    def list(self, request):
        """产品列表（仅返回启用的产品，按排序字段排列）"""
        queryset = Product.objects.filter(is_active=True)
        return Response({
            'code': 200,
            'message': 'success',
            'data': ProductSerializer(queryset, many=True).data
        })
