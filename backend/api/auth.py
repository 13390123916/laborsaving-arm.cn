"""
API 密钥鉴权 - 自研 Token 认证与权限（不依赖第三方包）
支持两种传入方式：
  1) Authorization: Bearer <prefix>.<secret>
  2) 查询参数 / 请求体 ?api_key=<prefix>.<secret>
密钥哈希使用 Django 自带密码哈希存储，明文仅创建时返回一次。
"""
import secrets
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from .models import ApiKey

# 权限层级（数值越大权限越高）
SCOPE_ORDER = {'read': 1, 'write': 2, 'admin': 3}


def generate_api_key():
    """生成 API 密钥，返回 (明文key, 前缀, 哈希)"""
    prefix = secrets.token_hex(4)          # 8 位前缀，用于定位记录
    secret = secrets.token_urlsafe(32)     # 密钥主体
    plain = f'{prefix}.{secret}'
    return plain, prefix, make_password(secret)


class ApiKeyAuthentication(BaseAuthentication):
    """API 密钥认证类"""

    def authenticate(self, request):
        key = self._extract_key(request)
        if not key:
            return None  # 未携带密钥，交由后续权限判定（通常为 AllowAny）

        if '.' not in key:
            return None

        prefix, secret = key.split('.', 1)
        try:
            ak = ApiKey.objects.get(key_prefix=prefix, is_active=True)
        except ApiKey.DoesNotExist:
            raise AuthenticationFailed('无效的 API 密钥')

        if not check_password(secret, ak.key_hash):
            raise AuthenticationFailed('无效的 API 密钥')

        # 记录最后使用时间
        ak.last_used_at = timezone.now()
        ak.save(update_fields=['last_used_at'])

        # 将权限范围挂到 request，供权限类消费
        request.apikey_scope = ak.scopes
        return (ak, None)

    @staticmethod
    def _extract_key(request):
        auth = request.META.get('HTTP_AUTHORIZATION', '')
        if auth.startswith('Bearer '):
            return auth[7:].strip()
        # 查询参数 / 表单字段兜底
        return request.query_params.get('api_key') or (request.data.get('api_key') if hasattr(request, 'data') else None)


class ApiKeyPermission(BasePermission):
    """API 密钥权限类，按视图声明的 required_scope 校验层级"""
    REQUIRED_SCOPE = 'read'

    def has_permission(self, request, view):
        scope = getattr(request, 'apikey_scope', None)
        if not scope:
            return False
        required = getattr(view, 'required_scope', self.REQUIRED_SCOPE)
        return SCOPE_ORDER.get(scope, 0) >= SCOPE_ORDER.get(required, 1)
