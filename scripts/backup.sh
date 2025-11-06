#!/bin/bash
# Backup script for Bots EDI Environment

set -e

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="bots_backup_${DATE}"
ENV_DIR="env/default"

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "Starting Bots EDI backup..."
echo "Backup name: $BACKUP_NAME"

# Create temporary directory for backup
TEMP_DIR=$(mktemp -d)
BACKUP_PATH="$TEMP_DIR/$BACKUP_NAME"
mkdir -p "$BACKUP_PATH"

# Backup configuration
echo "Backing up configuration..."
cp -r "$ENV_DIR/config" "$BACKUP_PATH/"

# Backup user scripts
echo "Backing up user scripts..."
cp -r "$ENV_DIR/usersys" "$BACKUP_PATH/"

# Backup database
echo "Backing up database..."
mkdir -p "$BACKUP_PATH/database"
if [ -f "$ENV_DIR/botssys/sqlitedb/botsdb" ]; then
    cp "$ENV_DIR/botssys/sqlitedb/botsdb" "$BACKUP_PATH/database/"
fi

# Backup important system files
echo "Backing up system files..."
if [ -d "$ENV_DIR/botssys/data" ]; then
    cp -r "$ENV_DIR/botssys/data" "$BACKUP_PATH/" 2>/dev/null || true
fi

# Create archive
echo "Creating archive..."
cd "$TEMP_DIR"
tar -czf "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" "$BACKUP_NAME"

# Cleanup
rm -rf "$TEMP_DIR"

echo "✅ Backup completed: $BACKUP_DIR/${BACKUP_NAME}.tar.gz"

# Optional: Remove old backups (keep last 30 days)
find "$BACKUP_DIR" -name "bots_backup_*.tar.gz" -mtime +30 -delete 2>/dev/null || true

echo "Backup size: $(du -h "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" | cut -f1)"
