"""
信号处理 - 登录/登出/失败事件记录 + 后台登录暴力破解防护
使用 Django 内置缓存（LocMemCache）记录失败次数，达到阈值临时锁定 IP。
"""
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.core.cache import cache
from .models import LoginLog

# 暴力破解防护阈值（15 分钟内失败 5 次锁定 15 分钟）
MAX_FAILS = 5
LOCK_SECONDS = 900
WINDOW_SECONDS = 900


def get_client_ip(request):
    if not request:
        return None
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')


def get_ua(request):
    if not request:
        return ''
    ua = request.META.get('HTTP_USER_AGENT', '')
    return ua[:500]


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    LoginLog.objects.create(
        username=user.username, user=user, action='login',
        ip_address=ip, user_agent=get_ua(request)
    )
    # 登录成功清除该 IP 的失败计数与锁定
    if ip:
        cache.delete(f'login_fail_{ip}')
        cache.delete(f'login_block_{ip}')


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    if not user or not user.is_authenticated:
        return
    LoginLog.objects.create(
        username=user.username, user=user, action='logout',
        ip_address=get_client_ip(request), user_agent=get_ua(request)
    )


@receiver(user_login_failed)
def log_failed(sender, credentials, request, **kwargs):
    username = credentials.get('username', '') if isinstance(credentials, dict) else ''
    ip = get_client_ip(request)
    LoginLog.objects.create(
        username=username, action='failed',
        ip_address=ip, user_agent=get_ua(request)
    )
    if ip:
        fails = cache.get(f'login_fail_{ip}', 0) + 1
        cache.set(f'login_fail_{ip}', fails, WINDOW_SECONDS)
        if fails >= MAX_FAILS:
            cache.set(f'login_block_{ip}', True, LOCK_SECONDS)
