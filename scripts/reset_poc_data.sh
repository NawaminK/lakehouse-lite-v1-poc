#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'
This script removes persisted Docker volumes and local POC folders.
Use it only when you want to reset the local demo environment completely.
EOF

docker compose down -v
rm -rf warehouse notebooks

echo "POC data reset completed. Run 'docker compose up -d --build' to start again."
