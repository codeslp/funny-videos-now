#!/bin/bash
# ─────────────────────────────────────────────────────────────
# Funny Video Generator — Cron Setup
#
# Schedule:
#   2:00 AM CST  — Generate 3 new videos (source, script, render)
#  11:00 AM CST  — Publish 1 video (lunch break peak)
#   2:00 PM CST  — Publish 1 video (afternoon scroll peak)
#   6:00 PM CST  — Publish 1 video (evening prime time - HIGHEST engagement)
#
# Usage: bash setup_cron.sh
# ─────────────────────────────────────────────────────────────

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="/usr/bin/env python3"
SRC="$PROJECT_DIR/src"

echo "📋 Setting up cron jobs for Funny Video Generator"
echo "   Project: $PROJECT_DIR"
echo ""

# Build cron entries
CRON_ENTRIES="
# ─── Funny Video Generator ───────────────────────────────
# Nightly generation at 2 AM CST
0 2 * * * cd $PROJECT_DIR && $PYTHON $SRC/generate_overnight.py --count 3 >> $PROJECT_DIR/logs/cron_generate.log 2>&1

# Publish at optimal times (CST)
# 11:00 AM — Lunch break engagement peak
0 11 * * * cd $PROJECT_DIR && $PYTHON $SRC/publish_scheduled.py >> $PROJECT_DIR/logs/cron_publish.log 2>&1

# 2:00 PM — Afternoon scroll peak
0 14 * * * cd $PROJECT_DIR && $PYTHON $SRC/publish_scheduled.py >> $PROJECT_DIR/logs/cron_publish.log 2>&1

# 6:00 PM — Evening prime time (highest engagement)
0 18 * * * cd $PROJECT_DIR && $PYTHON $SRC/publish_scheduled.py >> $PROJECT_DIR/logs/cron_publish.log 2>&1
# ─── End Funny Video Generator ───────────────────────────
"

echo "Will add these cron jobs:"
echo "$CRON_ENTRIES"
echo ""

read -p "Install these cron jobs? (y/n): " confirm
if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    # Backup existing crontab
    crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S) 2>/dev/null

    # Remove any existing Funny Video Generator entries
    (crontab -l 2>/dev/null | grep -v "Funny Video Generator" | grep -v "generate_overnight" | grep -v "publish_scheduled" | grep -v "cron_generate" | grep -v "cron_publish" | grep -v "End Funny Video") > /tmp/crontab_clean

    # Add new entries
    echo "$CRON_ENTRIES" >> /tmp/crontab_clean
    crontab /tmp/crontab_clean
    rm /tmp/crontab_clean

    echo "✅ Cron jobs installed!"
    echo ""
    echo "Current crontab:"
    crontab -l
else
    echo "⏭️  Skipped. To install manually, run: crontab -e"
fi

echo ""
echo "📊 Schedule Summary (CST):"
echo "   🌙  2:00 AM  — Source news → Score → Generate scripts → Render via Veo"
echo "   🌤️ 11:00 AM  — Publish 1 video (lunch break peak)"
echo "   ☀️  2:00 PM  — Publish 1 video (afternoon peak)"
echo "   🌆  6:00 PM  — Publish 1 video (prime time - HIGHEST engagement)"
echo ""
echo "   = 3 videos/day across YouTube Shorts + Facebook Reels"
echo ""
echo "📁 Logs: $PROJECT_DIR/logs/"
echo "   - cron_generate.log"
echo "   - cron_publish.log"
