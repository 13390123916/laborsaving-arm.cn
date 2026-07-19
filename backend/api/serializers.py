"""
序列化器 - 数据序列化与验证
"""
from rest_framework import serializers
from django.conf import settings
from .models import (Article, Faq, Contact, SiteConfig, Product, Certificate,
                     Milestone, ArticleLike, Media, LoginLog, ApiKey, IpRule)


class SiteConfigSerializer(serializers.ModelSerializer):
    """站点配置序列化器"""
    class Meta:
        model = SiteConfig
        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):
    """文章列表序列化器"""
    cover_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'slug', 'title', 'seo_title', 'seo_keywords', 'seo_description',
                  'category', 'cover', 'cover_image_url', 'summary', 'author', 'views',
                  'is_top', 'created_at']

    def get_cover_image_url(self, obj):
        return obj.cover_image.url if obj.cover_image else None


class ArticleDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化器"""
    cover_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'slug', 'title', 'seo_title', 'seo_keywords', 'seo_description',
                  'category', 'cover', 'cover_image_url', 'summary', 'content', 'author',
                  'views', 'status', 'is_top', 'sort_order', 'created_at', 'updated_at']

    def get_cover_image_url(self, obj):
        return obj.cover_image.url if obj.cover_image else None


class FaqSerializer(serializers.ModelSerializer):
    """FAQ序列化器"""
    class Meta:
        model = Faq
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    """联系表单序列化器"""
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone', 'email', 'message', 'source',
                  'intent_region', 'budget_range', 'lead_source',
                  'is_handled', 'created_at']
        read_only_fields = ['id', 'is_handled', 'created_at']

    def validate_phone(self, value):
        """手机号简单验证"""
        if not value or len(value) < 6:
            raise serializers.ValidationError('请输入有效的联系电话')
        return value


class ProductSerializer(serializers.ModelSerializer):
    """产品序列化器"""
    class Meta:
        model = Product
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    """资质证书序列化器"""
    image_media_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Certificate
        fields = ['id', 'name', 'image_url', 'image_media_url', 'description',
                  'sort_order', 'is_active', 'created_at']

    def get_image_media_url(self, obj):
        return obj.image.url if obj.image else None


class MilestoneSerializer(serializers.ModelSerializer):
    """企业历程序列化器"""
    class Meta:
        model = Milestone
        fields = '__all__'


class ArticleLikeSerializer(serializers.ModelSerializer):
    """文章点赞序列化器"""
    class Meta:
        model = ArticleLike
        fields = ['id', 'article', 'ip_address', 'created_at']
        read_only_fields = ['id', 'ip_address', 'created_at']


class MediaSerializer(serializers.ModelSerializer):
    """媒体文件序列化器"""
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Media
        fields = ['id', 'title', 'url', 'file', 'media_type', 'file_size', 'mime_type',
                  'uploaded_by', 'created_at']
        read_only_fields = ['id', 'url', 'file_size', 'mime_type', 'created_at']

    def get_url(self, obj):
        return obj.url


class MediaUploadSerializer(serializers.ModelSerializer):
    """媒体上传序列化器（仅写入标题与文件）"""
    class Meta:
        model = Media
        fields = ['id', 'title', 'file', 'media_type', 'uploaded_by']


class LoginLogSerializer(serializers.ModelSerializer):
    """登录日志序列化器"""
    class Meta:
        model = LoginLog
        fields = ['id', 'username', 'user', 'action', 'ip_address', 'user_agent', 'created_at']


class ApiKeySerializer(serializers.ModelSerializer):
    """API 密钥列表序列化器（不返回明文与哈希）"""
    class Meta:
        model = ApiKey
        fields = ['id', 'name', 'key_prefix', 'scopes', 'is_active', 'last_used_at',
                  'created_by', 'created_at']
        read_only_fields = ['id', 'key_prefix', 'key_hash', 'last_used_at', 'created_at']


class ApiKeyCreateSerializer(serializers.ModelSerializer):
    """API 密钥创建序列化器（返回一次性的明文 key）"""
    plain_key = serializers.CharField(read_only=True)

    class Meta:
        model = ApiKey
        fields = ['id', 'name', 'scopes', 'plain_key', 'created_at']
        read_only_fields = ['id', 'created_at']


class IpRuleSerializer(serializers.ModelSerializer):
    """IP 规则序列化器"""
    class Meta:
        model = IpRule
        fields = ['id', 'ip_address', 'rule_type', 'scope', 'note', 'is_active', 'created_at']
