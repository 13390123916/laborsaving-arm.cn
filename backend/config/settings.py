"""
Django 项目主配置文件
LABOR-SAVING 气动助力机械臂企业官网 - 后端配置
技术栈：Django + SQLite + Django REST Framework
"""
from pathlib import Path
import os

# 项目根目录（backend/）
BASE_DIR = Path(__file__).resolve().parent.parent
# 项目仓库根目录（含 frontend/）
PROJECT_ROOT = BASE_DIR.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'labor_saving_arm_2024_django_secret_key_prod_safe_change_me')

# 调试模式：默认开启（开发），生产环境务必设为 False（环境变量 DEBUG=False）
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# 允许访问的主机，上线后通过环境变量 ALLOWED_HOSTS 限定为实际域名（逗号分隔）
ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS')
ALLOWED_HOSTS = ALLOWED_HOSTS_ENV.split(',') if ALLOWED_HOSTS_ENV else ['*']

# ===== 生产环境 SPA 托管配置 =====
# 设置 SERVE_SPA=True 环境变量后，Django 同时托管 Vue 构建产物
# AI 爬虫抓取 llms.txt / robots.txt / sitemap.xml 时无跨域问题
SERVE_SPA = os.environ.get('SERVE_SPA', 'False') == 'True'
FRONTEND_DIST_DIR = PROJECT_ROOT / 'frontend' / 'dist'
# 实际修改在 TEMPLATES 和 STATICFILES_DIRS 定义之后完成

# 应用注册
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方
    'rest_framework',
    'corsheaders',
    # 本地应用
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'api.middleware.SecurityMiddleware',  # 后台防爆破 + IP 黑白名单拦截
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 生产环境 SPA 配置生效（TEMPLATES 已定义）
if SERVE_SPA:
    STATICFILES_DIRS = [FRONTEND_DIST_DIR]
    TEMPLATES[0]['DIRS'].append(FRONTEND_DIST_DIR)

# ===== 数据库配置（SQLite 轻量化）=====
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===== Django REST Framework 配置 =====
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    # 限流速率（仅公开写接口——联系表单/点赞——在对应视图中按需启用 AnonRateThrottle）
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',
        'user': '100/minute',
    },
}

# ===== CORS 跨域配置（前后端分离）=====
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r'^https://.*\.laborsaving-arm\.cn$',
    r'^http://.*\.laborsaving-arm\.cn$',
]

# 国际化（默认中文）
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# 静态文件
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 默认自动字段
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===== 生产环境安全头（环境驱动，开发默认关闭）=====
# 上线部署时在环境变量中开启：SECURE_SSL_REDIRECT=True SECURE_COOKIES=True HSTS_SECONDS=31536000
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT') == 'True'
SECURE_HSTS_SECONDS = int(os.environ.get('HSTS_SECONDS', '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
SECURE_HSTS_PRELOAD = SECURE_HSTS_SECONDS > 0
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
# Cookie 安全（仅 HTTPS 传输）：生产设为 True
SESSION_COOKIE_SECURE = os.environ.get('SECURE_COOKIES') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('SECURE_COOKIES') == 'True'

# ===== 缓存（限流/防爆破计数使用，默认进程内内存缓存）=====
# 多进程/多机部署时建议改为 redis 等共享缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
