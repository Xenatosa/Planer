#!/usr/bin/env bash
# Baut viewer_v2.js (IIFE-Bundle) aus src/ mit der gepinnten Kette aus relief3d/bau/package.json
# (esbuild 0.24.2, three 0.170.0). NODE_DIR = Ordner mit node_modules (npm ci von bau/package*.json).
set -euo pipefail
HIER="$(cd "$(dirname "$0")" && pwd)"
NODE_DIR="${NODE_DIR:-/tmp/dv2_viewer/node}"
if [ ! -x "$NODE_DIR/node_modules/.bin/esbuild" ]; then
  mkdir -p "$NODE_DIR"; cp "$HIER/../../bau/package.json" "$HIER/../../bau/package-lock.json" "$NODE_DIR/"
  (cd "$NODE_DIR" && npm ci --no-audit --no-fund --silent)
fi
NODE_PATH="$NODE_DIR/node_modules" "$NODE_DIR/node_modules/.bin/esbuild" "$HIER/src/main.js" --bundle --minify --format=iife \
  --target=es2020 --legal-comments=none --outfile="$HIER/viewer_v2.js" --log-level=warning
sha256sum "$HIER/viewer_v2.js"
