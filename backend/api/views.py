"""
视图函数 - RESTful API 接口
所有接口统一返回格式：{code, message, data}
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import os
from .models import (Article, Faq, Contact, SiteConfig, Product, Certificate,
                     Milestone, ArticleLike, Media, LoginLog, ApiKey, IpRule)
from .serializers import (SiteConfigSerializer, ArticleListSerializer,
                          ArticleDetailSerializer, FaqSerializer, ContactSerializer,
                          ProductSerializer, CertificateSerializer, MilestoneSerializer,
                          ArticleLikeSerializer, MediaSerializer, LoginLogSerializer,
                          ApiKeySerializer, IpRuleSerializer)
from .auth import ApiKeyAuthentication, ApiKeyPermission, generate_api_key


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
        """文章详情（浏览量+1）——支持数字 ID 或 URL 别名 slug"""
        try:
            if pk and str(pk).isdigit():
                article = Article.objects.get(id=pk, status=1)
            else:
                article = Article.objects.get(slug=pk, status=1)
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
    def get_throttles(self):
        # 仅对提交表单限流，防止恶意刷量（匿名用户 10 次/分钟）
        if self.action == 'create':
            return [AnonRateThrottle()]
        return []

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


class CertificateViewSet(viewsets.ViewSet):
    """资质证书接口"""
    def list(self, request):
        """证书列表"""
        queryset = Certificate.objects.filter(is_active=True)
        return Response({
            'code': 200,
            'message': 'success',
            'data': CertificateSerializer(queryset, many=True).data
        })


class MilestoneViewSet(viewsets.ViewSet):
    """企业历程接口"""
    def list(self, request):
        """里程碑列表"""
        queryset = Milestone.objects.filter(is_active=True)
        return Response({
            'code': 200,
            'message': 'success',
            'data': MilestoneSerializer(queryset, many=True).data
        })


class ArticleLikeViewSet(viewsets.ViewSet):
    """文章点赞接口"""
    def get_throttles(self):
        # 点赞接口限流（匿名用户 30 次/分钟），防止刷赞
        if self.action == 'create':
            return [AnonRateThrottle()]
        return []

    def create(self, request):
        """点赞"""
        article_id = request.data.get('article')
        if not article_id:
            return Response({'code': 400, 'message': '缺少文章ID', 'data': None},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            article = Article.objects.get(id=article_id, status=1)
        except Article.DoesNotExist:
            return Response({'code': 404, 'message': '文章不存在', 'data': None},
                            status=status.HTTP_404_NOT_FOUND)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        # 防止同IP重复点赞
        existing = ArticleLike.objects.filter(article=article, ip_address=ip).first()
        if existing:
            return Response({'code': 200, 'message': '您已点过赞', 'data': {'liked': True}})
        ArticleLike.objects.create(article=article, ip_address=ip)
        return Response({
            'code': 200,
            'message': '点赞成功',
            'data': {'liked': True, 'total': ArticleLike.objects.filter(article=article).count()}
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def count(self, request):
        """获取点赞数"""
        article_id = request.query_params.get('article')
        if not article_id:
            return Response({'code': 400, 'message': '缺少文章ID', 'data': None},
                            status=status.HTTP_400_BAD_REQUEST)
        total = ArticleLike.objects.filter(article_id=article_id).count()
        return Response({
            'code': 200,
            'message': 'success',
            'data': {'article': int(article_id), 'total': total}
        })


# ===== 媒体图库接口 =====
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg'}
DOC_EXTS = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.csv'}


class MediaViewSet(viewsets.ViewSet):
    """媒体图库接口
    - 列表：公开（供前端选择封面/证书图）
    - 上传/删除：需 API 密钥（write / admin 权限）
    """
    authentication_classes = [ApiKeyAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            from rest_framework.permissions import AllowAny
            return [AllowAny()]
        self.required_scope = 'write' if self.action == 'upload' else 'admin'
        return [ApiKeyPermission()]

    def list(self, request):
        """媒体列表（可按类型筛选）"""
        queryset = Media.objects.all()
        mtype = request.query_params.get('type')
        if mtype:
            queryset = queryset.filter(media_type=mtype)
        return Response({
            'code': 200, 'message': 'success',
            'data': MediaSerializer(queryset, many=True).data
        })

    @action(detail=False, methods=['post'])
    def upload(self, request):
        """上传媒体文件（需 write 权限密钥）"""
        f = request.FILES.get('file')
        if not f:
            return Response({'code': 400, 'message': '缺少上传文件', 'data': None},
                            status=status.HTTP_400_BAD_REQUEST)
        title = request.data.get('title') or f.name
        ext = os.path.splitext(f.name)[1].lower()
        if ext in IMAGE_EXTS:
            mtype = 'image'
        elif ext in DOC_EXTS:
            mtype = 'document'
        else:
            mtype = 'video'
        media = Media(
            title=title, file=f, media_type=mtype,
            file_size=f.size, mime_type=f.content_type,
            uploaded_by=request.data.get('uploaded_by') or 'api'
        )
        media.save()
        return Response({
            'code': 200, 'message': '上传成功',
            'data': MediaSerializer(media).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        """删除媒体（需 admin 权限密钥）"""
        try:
            media = Media.objects.get(id=pk)
        except Media.DoesNotExist:
            return Response({'code': 404, 'message': '文件不存在', 'data': None},
                            status=status.HTTP_404_NOT_FOUND)
        media.file.delete(save=False)
        media.delete()
        return Response({'code': 200, 'message': '删除成功', 'data': None})


# ===== 登录日志接口（需 admin 权限密钥）=====
class LoginLogViewSet(viewsets.ViewSet):
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [ApiKeyPermission]
    required_scope = 'admin'

    def list(self, request):
        """登录日志列表"""
        queryset = LoginLog.objects.all()
        action_filter = request.query_params.get('action')
        if action_filter:
            queryset = queryset.filter(action=action_filter)
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        total = queryset.count()
        items = queryset[(page - 1) * page_size: page * page_size]
        return Response({
            'code': 200, 'message': 'success',
            'data': {'list': LoginLogSerializer(items, many=True).data,
                     'total': total, 'page': page, 'page_size': page_size}
        })


# ===== API 密钥管理接口（需 admin 权限密钥）=====
class ApiKeyViewSet(viewsets.ViewSet):
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [ApiKeyPermission]
    required_scope = 'admin'

    def list(self, request):
        """密钥列表（不含明文与哈希）"""
        return Response({
            'code': 200, 'message': 'success',
            'data': ApiKeySerializer(ApiKey.objects.all(), many=True).data
        })

    def create(self, request):
        """创建密钥（明文仅返回一次）"""
        name = request.data.get('name')
        scopes = request.data.get('scopes', 'read')
        if not name:
            return Response({'code': 400, 'message': '请填写密钥名称', 'data': None},
                            status=status.HTTP_400_BAD_REQUEST)
        if scopes not in ('read', 'write', 'admin'):
            scopes = 'read'
        plain, prefix, key_hash = generate_api_key()
        ak = ApiKey.objects.create(
            name=name, key_prefix=prefix, key_hash=key_hash,
            scopes=scopes, created_by='api'
        )
        return Response({
            'code': 200, 'message': '创建成功，请妥善保存密钥（明文仅显示一次）',
            'data': {'id': ak.id, 'name': ak.name, 'scopes': ak.scopes, 'plain_key': plain}
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        """删除密钥"""
        ak = self._get(pk)
        if not ak:
            return Response({'code': 404, 'message': '密钥不存在', 'data': None},
                            status=status.HTTP_404_NOT_FOUND)
        ak.delete()
        return Response({'code': 200, 'message': '删除成功', 'data': None})

    @action(detail=True, methods=['patch'])
    def disable(self, request, pk=None):
        """启用/停用密钥"""
        ak = self._get(pk)
        if not ak:
            return Response({'code': 404, 'message': '密钥不存在', 'data': None},
                            status=status.HTTP_404_NOT_FOUND)
        ak.is_active = not ak.is_active
        ak.save(update_fields=['is_active'])
        return Response({'code': 200, 'message': '状态已更新', 'data': {'is_active': ak.is_active}})

    @staticmethod
    def _get(pk):
        try:
            return ApiKey.objects.get(id=pk)
        except ApiKey.DoesNotExist:
            return None


# ===== IP 黑白名单接口（需 admin 权限密钥）=====
class IpRuleViewSet(viewsets.ViewSet):
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [ApiKeyPermission]
    required_scope = 'admin'

    def list(self, request):
        """规则列表"""
        return Response({
            'code': 200, 'message': 'success',
            'data': IpRuleSerializer(IpRule.objects.all(), many=True).data
        })

    def create(self, request):
        """新增规则"""
        serializer = IpRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 200, 'message': '添加成功', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        """删除规则"""
        rule = self._get(pk)
        if not rule:
            return Response({'code': 404, 'message': '规则不存在', 'data': None},
                            status=status.HTTP_404_NOT_FOUND)
        rule.delete()
        return Response({'code': 200, 'message': '删除成功', 'data': None})

    @action(detail=True, methods=['patch'])
    def disable(self, request, pk=None):
        """启用/停用规则"""
        rule = self._get(pk)
        if not rule:
            return Response({'code': 404, 'message': '规则不存在', 'data': None},
                            status=status.HTTP_404_NOT_FOUND)
        rule.is_active = not rule.is_active
        rule.save(update_fields=['is_active'])
        return Response({'code': 200, 'message': '状态已更新', 'data': {'is_active': rule.is_active}})

    @staticmethod
    def _get(pk):
        try:
            return IpRule.objects.get(id=pk)
        except IpRule.DoesNotExist:
            return None
