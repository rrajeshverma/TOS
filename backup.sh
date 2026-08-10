#!/bin/bash

DATE=$(date +%F_%H-%M)

echo "📦 Running backup..."

# Git backup
git add .
git commit -m "Auto backup $DATE"
git push

# Create backups folder if not exists
mkdir -p backups

# Local zip backup
zip -r backups/TOS_$DATE.zip . > /dev/null

echo "✅ Backup completed"
