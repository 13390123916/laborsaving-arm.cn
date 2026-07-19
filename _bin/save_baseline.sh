#!/usr/bin/env bash
# ============================================================================
# save_baseline.sh —— 全局基线持久化 · 保存脚本（项目感知）
# ============================================================================
# 功能：
#   1. 将当前 /workspace 工程打包为一份带时间戳的基线快照（tar.gz）
#   2. 追加记录到项目 manifest.json（含 commit / sha256 / 父基线链）
#   3. 维护本地「完整克隆源」clone/（git pull，断网也可重建）
#   4. 镜像基线到 GitHub <baselines> 分支（跨会话持久、权威来源）
# 用法：
#   save_baseline.sh [项目slug] [描述]
#   无参时自动从 /workspace 的 git remote 推导项目 slug
# 设计原则：
#   - 追加式，永不删除历史基线（“不销毁历史工程基线”）
#   - 失败不破坏现有状态（set -u 但不 set -e 中途退出，关键步骤容错）
# ============================================================================
set -uo pipefail

ROOT="/root/.codebuddy/baselines"
WORK="/workspace"
TS="$(date +%Y%m%dT%H%M%S)"
DESC="${2:-auto}"

# ---------------------------------------------------------------------------
# 1. 解析项目 slug
# ---------------------------------------------------------------------------
detect_project() {
  local url
  url="$(cd "$WORK" 2>/dev/null && git config --get remote.origin.url 2>/dev/null || true)"
  if [ -z "$url" ]; then echo "default"; return; fi
  # 取路径最后一段去 .git，并把非字母数字点横线归一成 '-'
  local name
  name="$(basename "$url" .git)"
  echo "$name" | tr -c 'A-Za-z0-9' '-' | tr -s '-' | sed 's/^-//;s/-$//'
}
PROJECT="${1:-$(detect_project)}"
BASE="$ROOT/$PROJECT"
SNAP_DIR="$BASE/snapshots"
MIRROR="$BASE/mirror"
CLONE="$BASE/clone"
MANIFEST="$BASE/manifest.json"
mkdir -p "$SNAP_DIR"

log() { printf '[save-baseline %s] %s\n' "$(date +%H:%M:%S)" "$*"; }

# ---------------------------------------------------------------------------
# 2. 采集工程元信息
# ---------------------------------------------------------------------------
COMMIT="$(cd "$WORK" 2>/dev/null && git rev-parse --short HEAD 2>/dev/null || echo none)"
BRANCH="$(cd "$WORK" 2>/dev/null && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo none)"
DIRTY="$(cd "$WORK" 2>/dev/null && git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
REMOTE="$(cd "$WORK" 2>/dev/null && git config --get remote.origin.url 2>/dev/null || echo none)"

# 快照文件命名：baseline-<时间戳>.tar.gz
TAR="$SNAP_DIR/baseline-${TS}.tar.gz"

# ---------------------------------------------------------------------------
# 3. 打包 /workspace（排除版本库/缓存/大体积产物，保持快照轻量）
# ---------------------------------------------------------------------------
log "打包 /workspace -> $TAR"
tar \
  --exclude='.git' \
  --exclude='.codebuddy' \
  --exclude='node_modules' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.DS_Store' \
  --exclude='*.zip' \
  --exclude='*.tar.gz' \
  -czf "$TAR" -C "$WORK" . 2>/dev/null || {
    log "警告：打包存在部分不可读文件，已尽力打包"; }

SIZE="$(stat -c%s "$TAR" 2>/dev/null || echo 0)"
SHA="$(sha256sum "$TAR" 2>/dev/null | cut -d' ' -f1 || echo unknown)"

# ---------------------------------------------------------------------------
# 4. 维护本地完整克隆源（clone/）
# ---------------------------------------------------------------------------
if [ "$REMOTE" != "none" ] && [ -n "$REMOTE" ]; then
  if [ ! -d "$CLONE/.git" ]; then
    log "初始化本地完整克隆源：$CLONE"
    git clone --quiet "$REMOTE" "$CLONE" 2>/dev/null && log "克隆源初始化完成" || log "克隆源初始化失败（网络受限，可后续重试）"
  else
    ( cd "$CLONE" && git pull --ff-only --quiet 2>/dev/null ) && log "克隆源已更新(pull)" || log "克隆源 pull 跳过/失败"
  fi
fi

# ---------------------------------------------------------------------------
# 5. 更新 manifest.json（追加式，保留历史）
# ---------------------------------------------------------------------------
PREV="$( [ -f "$MANIFEST" ] && python3 - "$MANIFEST" <<'PY' 2>/dev/null
import json,sys
try:
    d=json.load(open(sys.argv[1]))
    lst=d.get("baselines",[])
    print(lst[-1]["id"] if lst else "none")
except Exception:
    print("none")
PY
)"
ID="bl-${TS}"
touch "$MANIFEST"
if [ ! -s "$MANIFEST" ]; then
  echo '{"project":"'"$PROJECT"'","remote":"'"$REMOTE"'","baselines":[]}' > "$MANIFEST"
fi
python3 - "$MANIFEST" "$ID" "$TS" "$COMMIT" "$BRANCH" "$DIRTY" "$SHA" "$SIZE" "$DESC" "$REMOTE" "$PREV" <<'PY'
import json,sys,datetime
p,id_,ts,commit,branch,dirty,sha,size,desc,remote,prev=sys.argv[1:12]
d=json.load(open(p))
entry={
  "id":id_,
  "ts":ts,
  "iso":datetime.datetime.now().isoformat(timespec="seconds"),
  "commit":commit,
  "branch":branch,
  "dirty_files":int(dirty or 0),
  "sha256":sha,
  "size_bytes":int(size or 0),
  "desc":desc,
  "remote":remote,
  "parent":prev,
  "snapshot":"snapshots/%s.tar.gz"%id_.replace("bl-","baseline-")
}
d.setdefault("baselines",[]).append(entry)
d["project"]=d.get("project") or "unknown"
d["remote"]=remote
d["updated"]=entry["iso"]
d["latest"]=id_
json.dump(d,open(p,"w"),ensure_ascii=False,indent=2)
print("manifest updated: latest=%s"%id_)
PY

# ---------------------------------------------------------------------------
# 6. 镜像到 GitHub <baselines> 分支（跨会话权威来源）
# ---------------------------------------------------------------------------
if [ "$REMOTE" != "none" ] && [ -n "$REMOTE" ]; then
  if [ ! -d "$MIRROR/.git" ]; then
    git init -q -b baselines "$MIRROR" 2>/dev/null
    ( cd "$MIRROR" && git remote add origin "$REMOTE" 2>/dev/null )
  fi
  # 复制快照 + manifest + 策略文档进镜像库
  mkdir -p "$MIRROR/snapshots"
  cp -f "$TAR" "$MIRROR/snapshots/" 2>/dev/null
  cp -f "$MANIFEST" "$MIRROR/manifest.json" 2>/dev/null
  cp -f "$ROOT/STRATEGY.md" "$MIRROR/STRATEGY.md" 2>/dev/null || true
  cp -rf "$ROOT/_bin" "$MIRROR/_bin" 2>/dev/null || true
  ( cd "$MIRROR" \
    && git add -A \
    && git -c user.email="baseline@local" -c user.name="BaselineBot" \
       commit -q -m "baseline: $ID (commit=$COMMIT dirty=$DIRTY)" 2>/dev/null \
    && git push -q -u origin baselines 2>/dev/null \
    && echo "[save-baseline] 已镜像到 GitHub <baselines> 分支" ) \
    || echo "[save-baseline] 镜像推送跳过/失败（网络受限，本地基线仍完整保留）"
fi

log "✅ 基线保存完成：项目=$PROJECT id=$ID commit=$COMMIT size=${SIZE}B sha=${SHA:0:12}"
log "   本地快照：$TAR"
log "   本地克隆源：$CLONE"
log "   历史基线数：$(python3 -c "import json;print(len(json.load(open('$MANIFEST')).get('baselines',[])))")"
