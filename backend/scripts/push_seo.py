#!/usr/bin/env python3
"""
SEO 主动推送脚本（7 天极速收录核心手段，深度研究报告 §6）

功能：
  1. 抓取线上 sitemap.xml 的全部 URL
  2. 主动推送给 百度搜索资源平台（data.zz.baidu.com/urls）—— 收录最快
  3. 推送给 IndexNow（Bing / 360 等实时索引）

用法：
  export SITE_URL=https://laborsaving-arm.cn
  export BAIDU_PUSH_TOKEN=你的百度推送token      # 百度站长平台「链接提交-主动推送」获取
  export INDEXNOW_KEY=你的IndexNow密钥          # https://www.indexnow.org 获取
  python3 backend/scripts/push_seo.py           # 推送全部 URL
  python3 backend/scripts/push_seo.py --url https://laborsaving-arm.cn/news/21  # 推送单条（发新文章后）

说明：
  - 凭证缺失的通道自动跳过（不报错），便于在未配置时安全调用。
  - 百度每日配额有限，建议：新文章发布后即时推送该条；全量推送用于新站首推/普查。
"""
import os
import sys
import argparse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

SITE_URL = os.environ.get('SITE_URL', 'https://laborsaving-arm.cn').rstrip('/')
BAIDU_PUSH_TOKEN = os.environ.get('BAIDU_PUSH_TOKEN', '')
INDEXNOW_KEY = os.environ.get('INDEXNOW_KEY', '')

USER_AGENT = 'Mozilla/5.0 (compatible; LaborsavingSEO/1.0)'


def fetch_sitemap_urls():
    """抓取 sitemap.xml 中的全部 <loc> URL"""
    sm_url = f'{SITE_URL}/sitemap.xml'
    try:
        req = urllib.request.Request(sm_url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read().decode('utf-8')
        root = ET.fromstring(data)
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        locs = [n.text for n in root.findall('.//s:loc', ns) if n.text]
        return locs
    except Exception as e:  # noqa
        print(f'  [warn] 抓取 sitemap 失败：{e}')
        return []


def push_baidu(urls):
    if not BAIDU_PUSH_TOKEN:
        print('  [skip] 未配置 BAIDU_PUSH_TOKEN，跳过百度推送')
        return None
    api = f'http://data.zz.baidu.com/urls?site={SITE_URL}&token={BAIDU_PUSH_TOKEN}'
    body = '\n'.join(urls).encode('utf-8')
    req = urllib.request.Request(api, data=body, headers={
        'User-Agent': USER_AGENT, 'Content-Type': 'text/plain'})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return f'HTTP {e.code}: {e.read().decode("utf-8", "ignore")}'


def push_indexnow(urls):
    if not INDEXNOW_KEY:
        print('  [skip] 未配置 INDEXNOW_KEY，跳过 IndexNow 推送')
        return None
    api = 'https://api.indexnow.org/indexnow'
    payload = {'host': SITE_URL.replace('https://', '').replace('http://', ''),
               'key': INDEXNOW_KEY, 'urlList': urls}
    import json
    req = urllib.request.Request(api, data=json.dumps(payload).encode('utf-8'),
                                 headers={'User-Agent': USER_AGENT,
                                          'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return f'HTTP {resp.status}'
    except urllib.error.HTTPError as e:
        return f'HTTP {e.code}: {e.read().decode("utf-8", "ignore")}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', help='仅推送单条 URL（覆盖 sitemap 抓取）')
    args = ap.parse_args()

    if args.url:
        urls = [args.url]
    else:
        print(f'抓取 sitemap：{SITE_URL}/sitemap.xml')
        urls = fetch_sitemap_urls()
        if not urls:
            print('未获取到任何 URL，退出。')
            sys.exit(1)
        print(f'共 {len(urls)} 条 URL')

    print('--- 百度主动推送 ---')
    r = push_baidu(urls)
    print('  结果：', r)

    print('--- IndexNow 推送 ---')
    r = push_indexnow(urls)
    print('  结果：', r)

    print('完成。建议：百度/360/搜狗站长平台完成验证后，再运行本脚本以触发收录。')


if __name__ == '__main__':
    main()
