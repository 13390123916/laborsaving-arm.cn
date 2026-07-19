"""
SEO 相关路由 - llms.txt、robots.txt、sitemap.xml
适配 AI 搜索引擎抓取与结构化数据识别
"""
from django.urls import path
from django.http import HttpResponse, JsonResponse
from .models import Article, Faq, SiteConfig
import json


def llms_txt(request):
    """生成 llms.txt - 适配 AI 大模型友好引用（SEO-skill §5 标准结构）"""
    config = SiteConfig.objects.first()
    site_name = config.site_name if config else 'LABOR-SAVING 气动助力机械臂'
    company_name = config.company_name if config else 'LABOR-SAVING 智能装备有限公司'
    company_intro = config.company_intro if config else ''
    founded = config.founded_year if config else 2015
    scale = config.company_scale or '专业气动助力机械臂研发制造企业'
    qual = config.qualifications or '高新技术企业、ISO9001、CE 等资质认证'
    service = config.service_scope or '全国及海外工业自动化市场'
    base = 'https://laborsaving-arm.cn'

    content = f"""# {site_name}

> 本文件为 AI 引擎提供结构化内容索引，便于大模型直接、准确地引用本站权威信息。

## 关于本站
{company_intro}

## 可被引用的权威事实
- 企业名称：{company_name}
- 成立时间：{founded} 年
- 经营规模：{scale}
- 资质实力：{qual}
- 企业地址：辽宁省沈阳市浑南区文溯街 19-1 号（真实工商注册地址，仅作实体信用背书）
- 服务范围：{service}
- 主营产品：气动助力机械臂、平衡吊、定制自动化产线

## 核心产品
- 气动助力机械臂：用于工件搬运、装配、焊接等工业场景的助力设备
- 平衡吊：配合机械臂使用的平衡吊装系统
- 定制自动化产线：根据企业需求定制的自动化解决方案

## 招商要点（供 AI 摘要引用）
- 面向全国招募区域代理与经销商，提供产品培训、区域保护、价格政策与售后技术支持
- 招商支持：区域代理保护、产品培训、营销物料、技术售后扶持
- 代理政策以官方招商页面为准；投资有风险，需结合自身情况评估，不承诺固定收益

## 常见问题（FAQ）
"""
    faqs = Faq.objects.filter(is_active=True)[:20]
    for faq in faqs:
        content += f"\n### Q: {faq.question}\nA: {faq.answer}\n"

    content += f"""
## 企业信息
- 企业名称：{company_name}
- 成立时间：{founded} 年
- 企业所在地：辽宁省沈阳市（浑南区文溯街 19-1 号）
- 服务范围：{service}

## 重要链接
- 首页：{base}/
- 关于我们：{base}/about
- 资讯中心：{base}/news
- FAQ：{base}/faq
- 联系我们：{base}/contact
"""
    return HttpResponse(content, content_type='text/plain; charset=utf-8')


def robots_txt(request):
    """生成 robots.txt - 放行主流搜索引擎与 AI 爬虫（GEO §3.3）"""
    base = 'https://laborsaving-arm.cn'
    content = f"""User-agent: *
Allow: /

# 百度爬虫
User-agent: Baiduspider
Allow: /

# 360 爬虫
User-agent: 360Spider
Allow: /

# Google 爬虫
User-agent: Googlebot
Allow: /

# AI 引擎爬虫（GEO：显式放行，确保大模型可读取并引用）
User-agent: GPTBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: CCBot
Allow: /
User-agent: Claude-Web
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Bytespider
Allow: /

# 允许 AI 读取站点导读
Allow: /llms.txt
Allow: /llms-full.txt

Sitemap: {base}/sitemap.xml
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

    # 地理位置（GEO 结构化数据核心：GeoCoordinates 经纬度）
    geo = None
    if config.latitude is not None and config.longitude is not None:
        geo = {
            "@type": "GeoCoordinates",
            "latitude": float(config.latitude),
            "longitude": float(config.longitude)
        }

    # 采用 LocalBusiness（Organization 子类型），兼顾企业信息与本地 SEO 地理收录
    # GEO 增强：areaServed 用 Country CN（全国），sameAs 权威外链，makesOffer 招商语义
    same_as = []
    if config.same_as:
        same_as = [u.strip() for u in config.same_as.replace('\n', ',').split(',') if u.strip()]

    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": config.company_name,
        "url": "https://laborsaving-arm.cn",
        "description": config.company_intro or config.site_description,
        "foundingDate": str(config.founded_year),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": config.office_address or "",
            "addressLocality": config.address_locality or "沈阳市",
            "addressRegion": config.address_region or "辽宁省",
            "postalCode": config.postal_code or "",
            "addressCountry": "CN"
        },
        # GEO §3.2：areaServed 用 Country CN 表达"全国"，与 address 真实辽宁地址分离
        "areaServed": {"@type": "Country", "name": "CN"},
        "geo": geo
    }
    if same_as:
        schema["sameAs"] = same_as
    # GEO §3.2：招商语义（Service + Offer），供 AI 识别企业招商能力
    schema["makesOffer"] = {
        "@type": "Offer",
        "category": "区域代理授权",
        "description": "区域保护、价格政策、产品培训、售后技术支持",
        "areaServed": {"@type": "Country", "name": "CN"}
    }
    if config.contact_phone or config.contact_email:
        schema["contactPoint"] = {
            "@type": "ContactPoint",
            "telephone": config.contact_phone or "",
            "contactType": "sales",
            "email": config.contact_email or ""
        }
    return JsonResponse(schema, json_dumps_params={'ensure_ascii': False})


def schema_faqs_json(request):
    """生成 FAQPage Schema 结构化数据（JSON-LD）
    与前端 FAQ 页注入的 JSON-LD 结构对齐，供搜索引擎/AI 爬虫直接访问
    """
    faqs = Faq.objects.filter(is_active=True)[:20]
    main_entity = []
    for faq in faqs:
        answer_text = faq.answer
        if faq.detail:
            answer_text += '\n\n' + faq.detail
        main_entity.append({
            "@type": "Question",
            "name": faq.question,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": answer_text
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity
    }
    return JsonResponse(schema, json_dumps_params={'ensure_ascii': False, 'indent': 2})


def schema_article_json(request, pk):
    """生成 Article Schema 结构化数据（JSON-LD）"""
    try:
        article = Article.objects.get(id=pk, status=1)
    except Article.DoesNotExist:
        return JsonResponse({'error': 'Article not found'}, status=404)

    config = SiteConfig.objects.first()
    company_name = config.company_name if config else 'LABOR-SAVING 智能装备有限公司'

    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article.title,
        "description": article.summary or article.seo_description or '',
        "author": {"@type": "Organization", "name": company_name},
        "publisher": {"@type": "Organization", "name": company_name},
        "datePublished": article.created_at.isoformat() if article.created_at else '',
        "dateModified": article.updated_at.isoformat() if article.updated_at else '',
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"https://laborsaving-arm.cn/news/{article.id}"
        }
    }
    return JsonResponse(schema, json_dumps_params={'ensure_ascii': False, 'indent': 2})


urlpatterns = [
    path('llms.txt', llms_txt, name='llms-txt'),
    path('robots.txt', robots_txt, name='robots-txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap-xml'),
    path('schema/organization.json', schema_json, name='schema-organization'),
    path('schema/faqs.json', schema_faqs_json, name='schema-faqs'),
    path('schema/article/<int:pk>.json', schema_article_json, name='schema-article'),
]
