"""
安全中间件 - 请求级防护
1) 后台登录暴力破解拦截（读取缓存中的临时锁定标记）
2) IP 黑白名单拦截（调用 ipguard）
仅做拦截判定，不处理业务逻辑；静态资源与媒体文件放行。
"""
from django.core.cache import cache
from django.http import HttpResponseForbidden


class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        # 静态/媒体/接口文档等非受限路径直接放行
        if path.startswith(('/static/', '/media/', '/favicon.ico')):
            return self.get_response(request)

        ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() \
            or request.META.get('REMOTE_ADDR')

        # 1) 后台登录暴力破解锁定
        if path.startswith('/admin/') and cache.get(f'login_block_{ip}'):
            return HttpResponseForbidden(
                '登录尝试过于频繁，账号已被临时锁定，请 15 分钟后再试。'
            )

        # 2) IP 黑白名单
        from .ipguard import check_ip_rule
        if check_ip_rule(path, ip):
            return HttpResponseForbidden('访问被拒绝（IP 访问规则限制）')

        return self.get_response(request)
