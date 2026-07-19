#!/usr/bin/env bash
# 后端 API + SEO 路由探测脚本（调试用）
# 路径基于脚本自身位置，克隆到任意目录均可运行
set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/backend"

# 启动后端
python3 manage.py runserver 127.0.0.1:8000 > /tmp/django.log 2>&1 &
SRV=$!
# 等待启动
for i in $(seq 1 30); do
  if curl -s -o /dev/null http://127.0.0.1:8000/api/site-config/info/; then break; fi
  sleep 1
done

B="http://127.0.0.1:8000"
echo "================ API / SEO 探测 ================"
probe() {
  local method="${1:-GET}"; local path="${2:-/}"; local body="${3:-}"
  local code
  if [ "$method" = "POST" ]; then
    code=$(curl -s -o /tmp/resp.txt -w "%{http_code}" -X POST "$B$path" -H "Content-Type: application/json" -d "$body")
  else
    code=$(curl -s -o /tmp/resp.txt -w "%{http_code}" "$B$path")
  fi
  local size; size=$(wc -c < /tmp/resp.txt)
  printf "%-6s %-38s -> HTTP %s | %s bytes\n" "$method" "$path" "$code" "$size"
}

probe GET  /api/site-config/info/
probe GET  /api/articles/
probe GET  /api/articles/categories/
probe GET  /api/articles/1/
probe GET  /api/articles/9999/
probe GET  /api/faqs/
probe GET  /api/products/
probe GET  /api/certificates/
probe GET  /api/milestones/
probe GET  /api/contacts/stats/
probe POST /api/contacts/ '{"name":"测试用户","phone":"13800000000","message":"调试测试留言","source":"/contact"}'
probe POST /api/contacts/ '{"name":"","phone":"1","message":""}'
probe POST /api/article-likes/ '{"article":1}'
probe GET  /llms.txt
probe GET  /robots.txt
probe GET  /sitemap.xml
probe GET  /schema/organization.json
probe GET  /schema/faqs.json
probe GET  /schema/article/1.json
probe GET  /schema/article/9999.json

echo
echo "================ 关键响应体检查 ================"
echo "--- site-config (地理/GEO/验证字段) ---"
curl -s "$B/api/site-config/info/" | python3 -c "import sys,json;d=json.load(sys.stdin)['data'];print('company:',d.get('company_name'));print('address:',d.get('office_address'));print('region/locality:',d.get('address_region'),'/',d.get('address_locality'));print('lat/lng:',d.get('latitude'),'/',d.get('longitude'));print('geo region fallback check:'); print('baidu_tongji:',d.get('baidu_tongji'));print('baidu_verify:',d.get('baidu_verify'));print('qihu_verify:',d.get('qihu_verify'));print('sogou_verify:',d.get('sogou_verify'));print('google_verify:',d.get('google_verify'));print('gtm_id:',d.get('gtm_id'));print('google_ga_id:',d.get('google_ga_id'))" 2>&1 | head -30

echo
echo "--- schema/organization.json ---"
curl -s "$B/schema/organization.json" | python3 -m json.tool 2>&1 | head -40

echo
echo "--- sitemap.xml ---"
curl -s "$B/sitemap.xml"

kill $SRV 2>/dev/null
echo
echo "================ Django 启动日志(尾部) ================"
tail -20 /tmp/django.log
