#!/usr/bin/env bash
# Usage: ./log.sh [package] [logfile]
set -euo pipefail

APP="${1:-app.komikku}"
LOG_FILE="${2:-extension-debug.log}"

# Android system/OS tags unrelated to app or extension code.
NOISE_TAGS='Zygote|zygote64|RenderThread|ViewRootImpl|SQLiteLog|\bLB\s*:|ziparchive|libEGL|OpenGLRenderer|FinalizerDaemon|IconCustomizer|\bLooper\s*:|RenderInspector|\blibc\s*:|\bSystem\s*:'

PID=$(adb shell pidof "$APP" | tr -d '\r' || true)
if [ -z "$PID" ]; then
    echo "App '$APP' is not running (start/open it on the device first)" >&2
    exit 1
fi

echo "Capturing PID $PID (system noise filtered) to $LOG_FILE (Ctrl-C to stop)"
adb logcat --pid="$PID" -v threadtime \
    | grep -v -E --line-buffered "$NOISE_TAGS" \
    | tee "$LOG_FILE"
