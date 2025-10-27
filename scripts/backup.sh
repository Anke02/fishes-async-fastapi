#!/usr/bin/env bash
set -e

BACKUP_DIR="${BACKUP_DIR:-./backups}"
BACKUP_NAME="${1:-backup_$(date +%Y%m%d_%H%M%S)}"
BACKUP_FILE="${BACKUP_DIR}/${BACKUP_NAME}.sql"

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

mkdir -p "$BACKUP_DIR"

echo "Creating backup: ${BACKUP_FILE}"

DB_USER="${POSTGRES_USER:-app}"
DB_PASSWORD="${POSTGRES_PASSWORD:-app}"
DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-app}"

PGPASSWORD="$DB_PASSWORD" pg_dump \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -F p \
    -f "$BACKUP_FILE"

echo "Backup created: ${BACKUP_FILE}"
echo "Size: $(du -h "$BACKUP_FILE" | cut -f1)"

BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/*.sql 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -gt 10 ]; then
    echo "Removing old backups (keeping last 10)..."
    ls -1t "$BACKUP_DIR"/*.sql | tail -n +11 | xargs rm -f
fi
