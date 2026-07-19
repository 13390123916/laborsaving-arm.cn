#!/bin/bash
# ==============================================
# 数据备份与恢复脚本 - LABOR-SAVING 企业官网
# 用法:
#   bash scripts/backup.sh backup    # 创建备份
#   bash scripts/backup.sh restore   # 恢复最新备份
#   bash scripts/backup.sh list      # 列出备份文件
# ==============================================

set -e

BACKUP_DIR="backups"
DB_FILE="db.sqlite3"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p "$BACKUP_DIR"

case "${1:-backup}" in
  backup)
    if [ ! -f "$DB_FILE" ]; then
      echo "❌ 数据库文件 $DB_FILE 不存在"
      exit 1
    fi
    BACKUP_FILE="${BACKUP_DIR}/db_${TIMESTAMP}.sqlite3"
    cp "$DB_FILE" "$BACKUP_FILE"
    echo "✅ 备份完成: $BACKUP_FILE ($(du -h "$BACKUP_FILE" | cut -f1))"
    # 保留最近30天的备份，自动清理更早的
    find "$BACKUP_DIR" -name "db_*.sqlite3" -mtime +30 -delete
    ;;
  restore)
    LATEST=$(ls -t ${BACKUP_DIR}/db_*.sqlite3 2>/dev/null | head -1)
    if [ -z "$LATEST" ]; then
      echo "❌ 未找到备份文件"
      exit 1
    fi
    if [ -f "$DB_FILE" ]; then
      cp "$DB_FILE" "${BACKUP_DIR}/db_before_restore_${TIMESTAMP}.sqlite3"
      echo "ℹ️  已备份当前数据库至 ${BACKUP_DIR}/db_before_restore_${TIMESTAMP}.sqlite3"
    fi
    cp "$LATEST" "$DB_FILE"
    echo "✅ 已从 $LATEST 恢复"
    ;;
  list)
    echo "📋 备份文件列表:"
    ls -lh "${BACKUP_DIR}/db_"*.sqlite3 2>/dev/null | awk '{print $NF, "("$5")"}' || echo "   无备份文件"
    ;;
  *)
    echo "用法: $0 {backup|restore|list}"
    exit 1
    ;;
esac
