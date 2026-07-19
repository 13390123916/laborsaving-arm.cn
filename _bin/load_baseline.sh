#!/usr/bin/env bash
# ============================================================================
# load_baseline.sh —— 全局基线持久化 · 加载脚本（项目感知）
# ============================================================================
# 功能：
#   将「最新」或「指定」基线快照干净恢复到 /workspace，
#   用于新建对话优先加载上一次同项目基线 / 会话恢复 / 回滚。
# 用法：
#   load_baseline.sh [项目slug] [latest|<基线id>] [--force]
# 安全原则：
#   - 恢复前若 /workspace 存在未提交改动，先自动存一份安全快照（不丢历史）
#   - 仅清理工程文件，永久保留 .codebuddy（agent 元数据）与 .git（版本历史）
#   - 历史基线永不删除，可随时回滚到任意 id
#   - 兜底：本地快照缺失时，自动从远程仓库（main）拉回完整工程
# ============================================================================
set -uo pipefail

ROOT="/root/.codebuddy/baselines"
WORK="/workspace"

detect_project() {
  local url
  url="$(cd "$WORK" 2>/dev/null && git config --get remote.origin.url 2>/dev/null || true)"
  [ -z "$url" ] && { echo "default"; return; }
  echo "$(basename "$url" .git)" | tr -c 'A-Za-z0-9' '-' | tr -s '-' | sed 's/^-//;s/-$//'
}
PROJECT="${1:-$(detect_project)}"
BASE="$ROOT/$PROJECT"
MANIFEST="$BASE/manifest.json"
SNAP_DIR="$BASE/snapshots"
CLONE="$BASE/clone"
FORCE=0
TARGET="latest"
[ "${2:-}" = "--force" ] && { FORCE=1; TARGET="latest"; }
[ "${3:-}" = "--force" ] && FORCE=1
[ -n "${2:-}" ] && [ "${2:-}" != "--force" ] && TARGET="$2"

log() { printf '[load-baseline %s] %s\n' "$(date +%H:%M:%S)" "$*"; }

if [ ! -f "$MANIFEST" ]; then
  echo "❌ 未找到项目 [$PROJECT] 的基线 manifest：$MANIFEST"; exit 1
fi

# 解析目标基线 id
ID="$(python3 - "$MANIFEST" "$TARGET" <<'PY'
import json,sys
m,target=sys.argv[1:3]
d=json.load(open(m))
bl=d.get("baselines",[])
if not bl:
    print("none"); sys.exit(0)
if target in ("latest",""):
    print(bl[-1]["id"]); sys.exit(0)
for e in bl:
    if e["id"]==target:
        print(e["id"]); sys.exit(0)
print("missing")
PY
)"
if [ "$ID" = "none" ] || [ "$ID" = "missing" ]; then
  echo "❌ 目标基线不存在：target=$TARGET"; exit 1
fi

# 解析该基线快照路径与元信息
SNAP="$(python3 - "$MANIFEST" "$ID" <<'PY'
import json,sys,os
m,id_=sys.argv[1:3]
d=json.load(open(m))
for e in d["baselines"]:
    if e["id"]==id_:
        print(e["snapshot"]); break
PY
)"
TAR="$BASE/$SNAP"
RESTORED_VIA_REMOTE=0

# 本地快照缺失时的兜底：从远程仓库（main）拉回完整工程，保证沙箱重置也能恢复
if [ ! -f "$TAR" ]; then
  log "⚠️ 本地快照缺失，尝试从远程仓库兜底恢复..."
  REMOTE="$(python3 -c "import json;print(json.load(open('$MANIFEST')).get('remote',''))" 2>/dev/null)"
  if [ -n "$REMOTE" ] && git ls-remote --heads "$REMOTE" >/dev/null 2>&1; then
    TMP="/tmp/_baseline_recover_$$"
    rm -rf "$TMP"
    if git clone --quiet "$REMOTE" "$TMP" 2>/dev/null; then
      find "$WORK" -mindepth 1 -maxdepth 1 ! -name '.codebuddy' ! -name '.git' -exec rm -rf {} + 2>/dev/null || true
      cp -a "$TMP/." "$WORK/" 2>/dev/null
      rm -rf "$TMP"
      RESTORED_VIA_REMOTE=1
      log "✅ 已从远程仓库恢复工程（main@latest）"
    else
      log "❌ 远程克隆失败"
    fi
  else
    log "❌ 无可用远程源"
  fi
  if [ "$RESTORED_VIA_REMOTE" -ne 1 ]; then
    echo "❌ 快照文件缺失且远程兜底失败：$TAR"; exit 1
  fi
fi

# 安全检查：/workspace 有未提交改动时，先存安全快照（除非 --force / 远程兜底路径）
DIRTY="$(cd "$WORK" 2>/dev/null && git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
if [ "$RESTORED_VIA_REMOTE" -ne 1 ] && [ "${DIRTY:-0}" -gt 0 ] && [ "$FORCE" -ne 1 ]; then
  SAFE="$SNAP_DIR/safety-preload-$(date +%Y%m%dT%H%M%S).tar.gz"
  tar --exclude='.git' --exclude='.codebuddy' -czf "$SAFE" -C "$WORK" . 2>/dev/null
  log "⚠️ 检测到 $DIRTY 个未提交改动，已先存安全快照：$SAFE"
  log "   如需丢弃改动直接恢复，请加 --force 参数"
fi

# 干净恢复：仅当未走远程兜底时，清理工程文件并解包快照
if [ "$RESTORED_VIA_REMOTE" -ne 1 ]; then
  log "清理 /workspace 工程文件（保留 .codebuddy / .git）..."
  find "$WORK" -mindepth 1 -maxdepth 1 \
    ! -name '.codebuddy' ! -name '.git' -exec rm -rf {} + 2>/dev/null || true
  log "解包基线 $ID -> $WORK"
  tar -xzf "$TAR" -C "$WORK" 2>/dev/null
fi

# 同步本地完整克隆源（若存在）
if [ -d "$CLONE/.git" ]; then
  ( cd "$CLONE" && git pull --ff-only --quiet 2>/dev/null ) && log "克隆源已同步" || true
fi

if [ "$RESTORED_VIA_REMOTE" -eq 1 ]; then
  log "✅ 基线加载完成（远程兜底）：项目=$PROJECT remote=$REMOTE"
else
  log "✅ 基线加载完成：项目=$PROJECT id=$ID"
  log "   快照：$TAR"
  log "   说明：$(python3 -c "import json;print([e['desc'] for e in json.load(open('$MANIFEST'))['baselines'] if e['id']=='$ID'][0])")"
fi
