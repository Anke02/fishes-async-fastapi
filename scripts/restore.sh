#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
    echo "Error: No backup file specified"
    echo "Usage: ./scripts/restore <backup_file>"
    echo ""
    echo "Available backups:"
    ls -lh backups/*.sql 2>/dev/null || echo "No backups found"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: File not found: ${BACKUP_FILE}"
    exit 1
fi

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Restoring backup: ${BACKUP_FILE}"

DB_USER="${POSTGRES_USER:-app}"
DB_PASSWORD="${POSTGRES_PASSWORD:-app}"
DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-app}"

read -p "Overwrite database '${DB_NAME}' on ${DB_HOST}? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 0
fi

echo "Dropping and recreating database..."
PGPASSWORD="$DB_PASSWORD" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d postgres \
    -c "DROP DATABASE IF EXISTS ${DB_NAME};"

PGPASSWORD="$DB_PASSWORD" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d postgres \
    -c "CREATE DATABASE ${DB_NAME};"

echo "Restoring data..."
PGPASSWORD="$DB_PASSWORD" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -f "$BACKUP_FILE"

echo "Restore completed from: ${BACKUP_FILE}"
