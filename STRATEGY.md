# 全局基线持久化策略（Global Baseline Persistence Strategy）

> 适用环境：本沙箱全部项目（Vue + Django + SQLite 企业官网等）。
> 生效日期：2025-07-19
> 目标：所有项目沙箱操作自动同步基线快照至本地缓存；新建对话优先加载上一次同项目基线；
> 会话超时 / 新建对话**不销毁**历史工程基线；本地磁盘留存完整克隆源。

---

## 一、核心原则

| 原则 | 说明 |
|------|------|
| **追加式持久** | 每次保存都生成**新**基线，历史基线永不删除、永不覆盖，可随时回滚到任意历史 id。 |
| **双保险存储** | 基线同时存在于 **本地缓存**（`/root/.codebuddy/baselines/`）与 **GitHub `<baselines>` 分支**（跨会话权威来源）。任一失效仍可重建。 |
| **完整克隆源** | 每个项目在本地保留一份完整 git 克隆（`clone/`），即使离线也能从本地重建工程，不依赖网络。 |
| **不破坏现场** | 加载基线前若 `/workspace` 存在未提交改动，自动先存一份安全快照；恢复过程永久保留 `.codebuddy` 与 `.git`。 |
| **可审计** | 每个基线在 `manifest.json` 中记录时间戳、commit、sha256、父基线链、描述，形成可追溯链。 |

---

## 二、目录结构（单一事实源布局）

```
/root/.codebuddy/baselines/                 # 全局基线根（跨休眠持久）
├── STRATEGY.md                             # 本策略文档
├── _bin/
│   ├── save_baseline.sh                    # 保存脚本（项目感知）
│   └── load_baseline.sh                    # 加载脚本（项目感知）
└── <project-slug>/                         # 每个项目独立隔离
    ├── manifest.json                       # 基线索引（追加式）
    ├── snapshots/                          # 历史基线快照 tar.gz（全部保留）
    │   ├── baseline-20250719T163700.tar.gz
    │   └── safety-preload-*.tar.gz         # 加载前自动安全快照
    ├── clone/                              # 本地完整克隆源（git pull 维护）
    └── mirror/                             # 镜像 git 仓库（baselines 分支）
```

> 项目 slug 由 `/workspace` 的 git remote 自动推导（如 `laborsaving-arm.cn` → `laborsaving-arm-cn`），
> 也可在调用脚本时显式传入。

---

## 三、自动同步触发条件

基线保存（`save_baseline.sh`）在以下时机自动执行：

1. **提交即基线**：`/workspace/.git/hooks/post-commit` 钩子，每次 `git commit` 后自动保存一份基线。
2. **任务收尾**：agent 完成任何修改 `/workspace` 的任务后，主动运行一次 `save_baseline.sh`。
3. **会话结束检查点**：长任务分阶段保存，避免单点丢失。

> 设计取舍：未采用常驻文件监听进程（跨会话不可靠）。以「git 提交钩子 + agent 主动保存」为自动同步主通道，
> 既保证实时性，又对沙箱生命周期零依赖。

---

## 四、新建对话 / 会话恢复流程（强制约定）

> **强制**：任何新开对话、会话超时恢复、或切换到本项目的对话，**第一步必须执行** `load_baseline.sh` 加载上一次同项目基线，再开始任何开发工作。本项目已在 `/workspace/AGENTS.md` 固化此约定，供所有对话（含非本次会话的 agent）遵循。

加载逻辑（自动判定，无需人工判断状态）：

1. 若本地快照存在 → 解包最新（或指定）基线到 `/workspace`，恢复前自动对未提交改动存安全快照，确保不丢工作。
2. **兜底**：若本地快照缺失（如沙箱被整体重置）→ 自动从远程仓库 `main` 分支克隆完整工程回 `/workspace`，保证工程永不丢失。
3. 若需回滚到历史基线 → `load_baseline.sh <project> <基线id>` 精准恢复（历史基线全部保留）。

```bash
# 恢复最新基线（项目自动识别，新对话首步必执行）
/root/.codebuddy/baselines/_bin/load_baseline.sh

# 指定项目 + 指定历史基线
/root/.codebuddy/baselines/_bin/load_baseline.sh laborsaving-arm-cn bl-20260719T164536

# 强制覆盖未提交改动
/root/.codebuddy/baselines/_bin/load_baseline.sh laborsaving-arm-cn latest --force
```

---

## 五、常用运维命令

```bash
# 保存当前工程为基线
/root/.codebuddy/baselines/_bin/save_baseline.sh [项目slug] [描述]

# 查看某项目全部基线
python3 -c "import json;[print(e['id'],e['ts'],e['commit'],e['desc']) for e in json.load(open('/root/.codebuddy/baselines/<project>/manifest.json'))['baselines']]"

# 列出本地所有项目基线
ls /root/.codebuddy/baselines/

# 查看 GitHub 基线分支
git ls-remote https://github.com/<owner>/<repo>.git 2>/dev/null | grep baselines
```

---

## 六、边界与说明

- **本地缓存目录**：`/root/.codebuddy` 跨沙箱休眠持久；若沙箱被整体重置，GitHub `<baselines>` 分支为唯一权威恢复源（需重新 `clone/` 初始化）。
- **快照体积**：打包已排除 `.git / node_modules / __pycache__ / *.zip / *.tar.gz` 等大体积对象，保持快照轻量、推送快速。
- **隐私/合规**：基线仅含工程源码与配置（符合项目合规约束），不含密钥或敏感凭据；若后续引入 `.env`，需在 `save_baseline.sh` 的排除列表中追加。
- **不销毁历史**：`manifest.json` 仅追加，`snapshots/` 仅增不删；如需清理旧基线，由人工显式操作，脚本不自动清理。
- **GitHub 镜像通道（已启用）**：写令牌经本地凭据文件 `/root/.codebuddy/baselines/.git-credentials`（权限 600）提供，`save_baseline.sh` 自动将 manifest + 最新快照 + 策略文档推送至 GitHub `<baselines>` 分支，作为跨会话权威恢复源；令牌不写入任何代码或日志。若令牌失效，脚本会自动跳过镜像、本地基线仍完整保留。
