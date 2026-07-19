"""
IP 黑白名单守卫 - 供安全中间件调用
支持纯 IP 与 CIDR（如 192.168.1.0/24）；命中黑名单即拦截，
若存在白名单则仅放行白名单内 IP（其余拦截）。结果缓存 60 秒降低查询开销。
"""
import ipaddress
from django.core.cache import cache
from .models import IpRule


def _ip_matches(ip, rule_str):
    """判断 ip 是否匹配规则（纯 IP 或 CIDR）"""
    if not rule_str:
        return False
    if '/' not in rule_str:
        return ip == rule_str
    try:
        return ipaddress.ip_address(ip) in ipaddress.ip_network(rule_str, strict=False)
    except ValueError:
        return False


def check_ip_rule(path, ip):
    """返回 True 表示应拦截该请求"""
    if not ip:
        return False

    scope = 'admin' if path.startswith('/admin/') else ('api' if path.startswith('/api/') else 'all')

    cache_key = f'iprules_{scope}'
    rules = cache.get(cache_key)
    if rules is None:
        active = IpRule.objects.filter(is_active=True, scope__in=[scope, 'all'])
        rules = [(r.rule_type, r.ip_address) for r in active]
        cache.set(cache_key, rules, 60)

    deny = [a for t, a in rules if t == 'deny']
    allow = [a for t, a in rules if t == 'allow']

    if any(_ip_matches(ip, a) for a in deny):
        return True

    if allow and not any(_ip_matches(ip, a) for a in allow):
        return True

    return False
