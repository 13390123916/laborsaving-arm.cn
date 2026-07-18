#!/bin/bash
# SSG 预渲染入口脚本
# 启动 vite preview -> 运行 prerender -> 关闭 preview
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

PREVIEW_PORT=4173
PREVIEW_HOST=127.0.0.1

echo "=== 启动预览服务器 ==="
pnpm exec vite preview --host $PREVIEW_HOST --port $PREVIEW_PORT --strictPort &
PREVIEW_PID=$!

# 等待服务器就绪
for i in $(seq 1 20); do
  if curl -s -o /dev/null "http://$PREVIEW_HOST:$PREVIEW_PORT/"; then
    echo "预览服务器已就绪 (PID: $PREVIEW_PID)"
    break
  fi
  sleep 0.5
done

echo ""
echo "=== 开始预渲染 ==="
node scripts/prerender.js --no-server

EXIT_CODE=$?

echo ""
echo "=== 关闭预览服务器 ==="
kill $PREVIEW_PID 2>/dev/null || true
wait $PREVIEW_PID 2>/dev/null || true

exit $EXIT_CODE
