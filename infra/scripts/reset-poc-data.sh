#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Stopping and removing POC volumes"
docker compose down -v

echo "Removing local generated folders"
rm -rf warehouse notebooks

echo "Reset completed. Run 'make up' to recreate the POC."
