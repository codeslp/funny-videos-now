#!/bin/bash
# ─────────────────────────────────────────────────────────────
# Funny Video Generator — launchd Setup for macOS
#
# Installs 4 LaunchAgents that:
#   ✅ Run even when your Mac wakes from sleep
#   ✅ Catch up on missed jobs automatically
#   ✅ Work with the display off
#
# Schedule (CST):
#   🌙  2:00 AM  — Generate 3 videos (source → score → script → render)
#   🌤️ 11:00 AM  — Publish 1 video (lunch break peak)
#   ☀️  2:00 PM  — Publish 1 video (afternoon peak)
#   🌆  6:00 PM  — Publish 1 video (evening prime time)
# ─────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_DIR="$SCRIPT_DIR/launchd"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
LOG_DIR="$(cd "$SCRIPT_DIR/.." && pwd)/logs"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  🎬  Funny Video Generator — launchd Setup"
echo "═══════════════════════════════════════════════════════"
echo ""

# Create logs directory
mkdir -p "$LOG_DIR"

# List of plists to install
PLISTS=(
    "com.funnyvideos.generate.plist"
    "com.funnyvideos.publish.morning.plist"
    "com.funnyvideos.publish.afternoon.plist"
    "com.funnyvideos.publish.evening.plist"
)

LABELS=(
    "com.funnyvideos.generate"
    "com.funnyvideos.publish.morning"
    "com.funnyvideos.publish.afternoon"
    "com.funnyvideos.publish.evening"
)

DESCRIPTIONS=(
    "🌙 2:00 AM  — Nightly video generation (3 videos)"
    "🌤️ 11:00 AM — Publish 1 video (lunch peak)"
    "☀️  2:00 PM  — Publish 1 video (afternoon peak)"
    "🌆 6:00 PM  — Publish 1 video (evening prime time)"
)

echo "  Will install these scheduled jobs:"
echo ""
for i in "${!DESCRIPTIONS[@]}"; do
    echo "    ${DESCRIPTIONS[$i]}"
done
echo ""

# Ensure LaunchAgents directory exists
mkdir -p "$LAUNCH_AGENTS"

for i in "${!PLISTS[@]}"; do
    plist="${PLISTS[$i]}"
    label="${LABELS[$i]}"
    src="$PLIST_DIR/$plist"
    dst="$LAUNCH_AGENTS/$plist"

    # Unload if already loaded
    launchctl list | grep -q "$label" && launchctl unload "$dst" 2>/dev/null

    # Copy plist to LaunchAgents
    cp "$src" "$dst"

    # Load it
    launchctl load "$dst"

    echo "  ✅ Installed: $label"
done

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  ✅ All 4 jobs installed and active!"
echo ""
echo "  📊 Daily Schedule (CST):"
echo "     🌙  2:00 AM — Generate 3 new videos"
echo "     🌤️ 11:00 AM — Publish video #1"
echo "     ☀️  2:00 PM — Publish video #2"
echo "     🌆  6:00 PM — Publish video #3"
echo ""
echo "  🔧 Manage:"
echo "     View:    launchctl list | grep funnyvideos"
echo "     Stop:    launchctl unload ~/Library/LaunchAgents/com.funnyvideos.*.plist"
echo "     Restart: bash $SCRIPT_DIR/setup_launchd.sh"
echo ""
echo "  📁 Logs: $LOG_DIR/"
echo "═══════════════════════════════════════════════════════"
echo ""
