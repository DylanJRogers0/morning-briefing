#!/bin/bash
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
  git -C "$CLAUDE_PROJECT_DIR" pull origin main --ff-only
fi
