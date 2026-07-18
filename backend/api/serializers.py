"""
序列化器 - 数据序列化与验证
"""
from rest_framework import serializers
from .models import Article, Faq, Contact, SiteConfig


class SiteConfigSerializer(serializers.ModelSerializer):
    """站点配置序列化器"""
    class Meta:
        model = SiteConfig
        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):
    """文章列表序列化器"""
    class Meta:
        model = Article
        fields = ['id', 'title', 'seo_title', 'seo_keywords', 'seo_description',
                  'category', 'cover', 'summary', 'author', 'views', 'is_top',
                  'created_at']


class ArticleDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化器"""
    class Meta:
        model = Article
        fields = '__all__'


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
                  'is_handled', 'created_at']
        read_only_fields = ['id', 'is_handled', 'created_at']

    def validate_phone(self, value):
        """手机号简单验证"""
        if not value or len(value) < 6:
            raise serializers.ValidationError('请输入有效的联系电话')
        return value
