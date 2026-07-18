"""
SEO 相关路由 - llms.txt、robots.txt、sitemap.xml
适配 AI 搜索引擎抓取与结构化数据识别
"""
from django.urls import path
from django.http import HttpResponse, JsonResponse
from .models import Article, Faq, SiteConfig
import json


def llms_txt(request):
    """生成 llms.txt - 适配 AI 大模型友好引用"""
    config = SiteConfig.objects.first()
    site_name = config.site_name if config else 'LABOR-SAVING 气动助力机械臂'
    company_intro = config.company_intro if config else ''
    content = f"""# {site_name}

> {company_intro}

## 关于本站
LABOR-SAVING 专注气动助力机械臂研发与生产，提供工业自动化助力解决方案。
本文件为 AI 引擎提供结构化内容索引，便于大模型友好引用。

## 核心产品
- 气动助力机械臂：用于工件搬运、装配、焊接等工业场景的助力设备
- 平衡吊：配合机械臂使用的平衡吊装系统
- 定制自动化产线：根据企业需求定制的自动化解决方案

## 常见问题（FAQ）
"""
    faqs = Faq.objects.filter(is_active=True)[:15]
    for faq in faqs:
        content += f"\n### Q: {faq.question}\nA: {faq.answer}\n"

    content += """
## 企业信息
- 企业名称：LABOR-SAVING 智能装备有限公司
- 成立时间：2015年
- 服务范围：全国及海外工业自动化市场

## 联系方式
- 咨询表单：/contact
- 了解更多：访问网站首页获取最新资讯

## 重要链接
- 首页：/
- 关于我们：/about
- 资讯中心：/news
- FAQ：/faq
"""
    return HttpResponse(content, content_type='text/plain; charset=utf-8')


def robots_txt(request):
    """生成 robots.txt"""
    content = """User-agent: *
Allow: /

# 百度爬虫
User-agent: Baiduspider
Allow: /

# Google 爬虫
User-agent: Googlebot
Allow: /

# AI 爬虫友好
User-agent: GPTBot
Allow: /
User-agent: CCBot
Allow: /
User-agent: ChatGPT-User
Allow: /

Sitemap: /sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain; charset=utf-8')


def sitemap_xml(request):
    """生成 sitemap.xml"""
    config = SiteConfig.objects.first()
    site_name = config.site_name if config else 'LABOR-SAVING'
    base_url = 'https://laborsaving-arm.cn'
    articles = Article.objects.filter(status=1)

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    # 静态页面
    for path in ['', '/about', '/news', '/faq', '/contact']:
        xml.append(f'  <url><loc>{base_url}/{path.lstrip("/")}</loc>'
                   f'<changefreq>weekly</changefreq><priority>0.8</priority></url>')
    # 文章页面
    for art in articles:
        xml.append(f'  <url><loc>{base_url}/news/{art.id}</loc>'
                   f'<lastmod>{art.updated_at.strftime("%Y-%m-%d")}</lastmod>'
                   f'<changefreq>monthly</changefreq><priority>0.6</priority></url>')
    xml.append('</urlset>')
    return HttpResponse('\n'.join(xml), content_type='application/xml; charset=utf-8')


def schema_json(request):
    """生成 Organization Schema 结构化数据（JSON-LD）"""
    config = SiteConfig.objects.first()
    if not config:
        config = SiteConfig.objects.create()

    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": config.company_name,
        "url": "https://laborsaving-arm.cn",
        "description": config.company_intro or config.site_description,
        "foundingDate": str(config.founded_year),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": config.office_address or "",
            "addressCountry": "CN"
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": config.contact_phone or "",
            "contactType": "sales",
            "email": config.contact_email or ""
        }
    }
    return JsonResponse(schema, json_dumps_params={'ensure_ascii': False})


urlpatterns = [
    path('llms.txt', llms_txt, name='llms-txt'),
    path('robots.txt', robots_txt, name='robots-txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap-xml'),
    path('schema/organization.json', schema_json, name='schema-organization'),
]
