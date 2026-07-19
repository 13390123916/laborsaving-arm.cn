"""API 应用配置 - 启动时注册信号"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # 注册登录审计与防爆破信号
        import api.signals  # noqa: F401
