#!/bin/bash
set -e

DATE=$(date +%Y-%m-%d)

echo "Starting backup: $DATE"

# Backup SQLite database
sqlite3 data/pod.db ".backup data/backup_${DATE}.db"
echo "Database backed up"

# Archive designs
tar -czf /tmp/designs_${DATE}.tar.gz data/designs/
echo "Designs archived"

# Upload to S3/Backblaze (if configured)
if [ -n "$S3_BUCKET" ] && [ -n "$S3_ACCESS_KEY" ]; then
    export AWS_ACCESS_KEY_ID="$S3_ACCESS_KEY"
    export AWS_SECRET_ACCESS_KEY="$S3_SECRET_KEY"

    ENDPOINT_FLAG=""
    if [ -n "$S3_ENDPOINT_URL" ]; then
        ENDPOINT_FLAG="--endpoint-url $S3_ENDPOINT_URL"
    fi

    aws s3 cp "data/backup_${DATE}.db" "s3://$S3_BUCKET/backups/" $ENDPOINT_FLAG
    aws s3 cp "/tmp/designs_${DATE}.tar.gz" "s3://$S3_BUCKET/backups/" $ENDPOINT_FLAG
    echo "Uploaded to S3"
else
    echo "S3 not configured, skipping upload"
fi

# Clean up old local backups (keep last 7)
ls -t data/backup_*.db 2>/dev/null | tail -n +8 | xargs rm -f
echo "Backup complete: $DATE"
